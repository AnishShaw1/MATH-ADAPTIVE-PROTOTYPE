# Technical Note — Math Adventures (Adaptive Prototype)

## 1. Architecture & Flow
- **User Interface (Console)**: `src/main.py` — prompts learner for name and initial difficulty, loops through puzzles, logs responses.
- **Puzzle Generator**: `src/puzzle_generator.py` — generates arithmetic problems tailored to difficulty (Easy/Medium/Hard).
- **Performance Tracker**: `src/tracker.py` — records each attempt (question, given answer, correct answer, correctness boolean, time taken, difficulty).
- **Adaptive Engine**: `src/adaptive_engine.py` — rule-based decision module that uses recent-window metrics to choose the next difficulty level.

Flow:
1. Learner selects start difficulty.
2. System presents puzzle at current difficulty.
3. Tracker logs correctness and response time.
4. Adaptive Engine examines the `window` most recent attempts and:
   - Raises difficulty if accuracy >= `up_inc_acc` and average time <= `slow_time_threshold`.
   - Lowers difficulty if accuracy <= `down_dec_acc` or avg time very high.
   - Otherwise keeps difficulty constant.
5. Repeat until session end. Show summary.

## 2. Adaptive Logic
**Rule-based approach (used here)**:
- Parameters:
  - window = 5 (recent attempts considered)
  - up_inc_acc = 0.8 (80% accuracy to increase)
  - down_dec_acc = 0.5 (50% or lower to decrease)
  - slow_time_threshold = 12s
- Rationale:
  - Simple, interpretable, and robust for small datasets / initial deployments.
  - Works well for keeping learners in the "zone of proximal development": increase challenge when consistently correct and fast, reduce when struggling or slow.

**ML alternative (optional)**:
- Collect features per-window: accuracy, avg_time, difficulty, time trend, streak length.
- Train a classifier/regressor (e.g., logistic regression, small decision tree) to predict next difficulty or probability to succeed at next level.
- Needs labeled data (historical sessions, teacher annotations) and strategies for dealing with noise.

## 3. Key Metrics Tracked
- **Correctness** (boolean) — primary signal for mastery.
- **Response time (seconds)** — provides secondary signal: very long times imply struggle or guesswork.
- **Recent accuracy** (last N attempts) and **average time** — used in adaptive rule.
- **Per-level counts & accuracy** — used in session summary.

How they influence difficulty:
- High recent accuracy + acceptable speed → increase level.
- Low recent accuracy or slow times → decrease level.
- Otherwise maintain current level.

## 4. Why rule-based for the prototype
- Interpretable for graders and interviewers.
- Works without large training datasets.
- Easier to explain trade-offs (threshold choice, window size).
- Low implementation complexity — meets assignment goals quickly.

## 5. Data collection & improvement
- **How to collect real data**: log anonymized session data (question, difficulty, correctness, response time, age group, timestamp) to a central database or CSV with user consent.
- **Improving models**:
  - Aggregate many sessions, engineer features (streaks, time-of-day, question-type difficulty).
  - Train lightweight models (decision tree / logistic regression) to predict success probability per-level; use models to personalize difficulty or recommend targeted practice.
- **Handling noisy or inconsistent performance**:
  - Use smoothing (exponential moving average), require streaks before increasing difficulty, add minimum attempt counts before change.
  - Reject outlier times (e.g., accidental idle) by capping max_time or ignoring top 5% durations.

## 6. Trade-offs: Rule-based vs ML-driven
- **Rule-based**: interpretable, robust with little data, easy to tune and explain. Risks: may be brittle for diverse learners; threshold choices might not generalize.
- **ML-driven**: can learn nuanced patterns, personalize more deeply. Risks: needs data, can overfit, less interpretable (though can use simple models), and requires infrastructure to collect and validate data.

## 7. Scaling beyond math
- Abstract puzzle generator to `Task` interface and plug topic-specific generators (spelling, reading comprehension, coding puzzles).
- Track domain-specific features (e.g., hint usage, partial credit).
- Adaptive engine can be reused; features can be extended per-discipline.

## 8. Summary
This lightweight prototype demonstrates an adaptive loop with clear logging and an interpretable decision engine. It is intentionally small to emphasize adaptive logic over UI; the code is modular to facilitate extension to ML-driven adaptation, web UI, or richer analytics.
