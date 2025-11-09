"""
main.py

Console interface:

- Ask name
- Choose initial difficulty (easy/medium/hard)
- Loop for N questions (or until user quits)
- Track correctness & response time
- AdaptiveEngine picks next difficulty
- Show final summary
"""

import time
from puzzle_generator import generate_puzzle
from tracker import Tracker
from adaptive_engine import AdaptiveEngine, LEVELS

def choose_initial_level():
    choices = {"1": "easy", "2": "medium", "3": "hard"}
    print("Choose initial difficulty: 1) Easy  2) Medium  3) Hard")
    while True:
        c = input("Enter 1/2/3 (default 1): ").strip() or "1"
        if c in choices:
            return choices[c]
        print("Invalid choice. Try again.")

def prompt_float(prompt_text):
    while True:
        v = input(prompt_text).strip()
        try:
            return float(v)
        except ValueError:
            print("Please enter a numeric answer (or type 'q' to quit).")
            if v.lower() == "q":
                raise KeyboardInterrupt

def run_session():
    print("=== Math Adventures — Adaptive Prototype ===")
    name = input("Enter learner name: ").strip() or "Learner"
    level = choose_initial_level()
    tracker = Tracker()
    engine = AdaptiveEngine(tracker)

    print(f"\nHi {name}! Starting at '{level.title()}' level.")
    print("Type 'q' anytime to finish and see summary.")
    num_questions = input("How many puzzles would you like? (default 10): ").strip()
    try:
        num_questions = int(num_questions) if num_questions else 10
    except ValueError:
        num_questions = 10

    q_count = 0
    try:
        while q_count < num_questions:
            q_count += 1
            q_text, correct_ans = generate_puzzle(level)
            print(f"\nQ{q_count} [{level.title()}]: {q_text}")
            start = time.perf_counter()
            raw = input("Your answer: ").strip()
            if raw.lower() == "q":
                break
            end = time.perf_counter()
            time_taken = end - start

            # attempt to parse numeric input
            try:
                given = float(raw)
            except ValueError:
                # mark as incorrect
                print(f"Invalid numeric input — counted as incorrect. Correct: {correct_ans}")
                tracker.log_attempt(q_text, raw, correct_ans, time_taken, level)
                # decide next
                next_level = engine.decide_next(level)
                print(f"-> Next level: {next_level.title()}")
                level = next_level
                continue

            # log
            tracker.log_attempt(q_text, given, correct_ans, time_taken, level)
            entry_correct = tracker.attempts[-1]["correct"]
            if entry_correct:
                print("Correct! ✅")
            else:
                print(f"Incorrect. Correct answer: {correct_ans}")

            # show short running stats for last window
            recent_acc = tracker.accuracy(engine.window)
            recent_time = tracker.average_time(engine.window)
            print(f"Recent accuracy (last {engine.window}): {recent_acc*100:.0f}%, avg time: {recent_time:.1f}s")

            # adaptive decision
            next_level = engine.decide_next(level)
            if next_level != level:
                print(f"Adaptive engine changes level: {level.title()} -> {next_level.title()}")
            else:
                print(f"Staying at {level.title()}.")
            level = next_level

    except KeyboardInterrupt:
        print("\nSession ended by user.")

    # final summary
    s = tracker.summary()
    print("\n=== Session Summary ===")
    print(f"Learner: {name}")
    print(f"Total attempts: {s['total']}")
    print(f"Overall accuracy: {s['accuracy']*100:.1f}%")
    print(f"Average time per question: {s['avg_time']:.2f}s")
    print("Per-level stats:")
    for lvl, st in s["level_stats"].items():
        print(f" - {lvl.title()}: {st['count']} Qs, accuracy {st['accuracy']*100:.1f}%")
    print("\nDifficulty transitions log (chronological):")
    for i, a in enumerate(tracker.attempts, 1):
        print(f"{i}. [{a['difficulty']}] {a['question']} -> given={a['given']} correct={a['correct']} time={a['time_taken']:.2f}s")
    print("\nRecommended next level based on recent performance:", engine.decide_next(level).title())
    print("Thanks for trying Math Adventures — keep practicing!")

if __name__ == "__main__":
    run_session()
