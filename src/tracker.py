"""
tracker.py

Simple tracker that logs each attempt with:
- question text
- provided answer
- correctness (bool)
- time_taken (seconds)
- difficulty level
"""

import time
from typing import List, Dict

class Tracker:
    def __init__(self):
        self.attempts: List[Dict] = []

    def log_attempt(self, question: str, given_answer: float, correct_answer: float,
                    time_taken: float, difficulty: str):
        correct = self._is_correct(given_answer, correct_answer)
        entry = {
            "question": question,
            "given": given_answer,
            "correct_answer": correct_answer,
            "correct": correct,
            "time_taken": time_taken,
            "difficulty": difficulty,
            "timestamp": time.time()
        }
        self.attempts.append(entry)

    @staticmethod
    def _is_correct(given, correct, tol=1e-6):
        # Accept small float error and integer rounding for division if close
        try:
            return abs(float(given) - float(correct)) <= tol
        except Exception:
            return False

    def accuracy(self, last_n: int = None):
        data = self.attempts[-last_n:] if last_n else self.attempts
        if not data:
            return 0.0
        return sum(1 for a in data if a["correct"]) / len(data)

    def average_time(self, last_n: int = None):
        data = self.attempts[-last_n:] if last_n else self.attempts
        if not data:
            return 0.0
        return sum(a["time_taken"] for a in data) / len(data)

    def summary(self):
        total = len(self.attempts)
        acc = self.accuracy() if total else 0.0
        avg_t = self.average_time() if total else 0.0
        by_level = {}
        for a in self.attempts:
            by_level.setdefault(a["difficulty"], []).append(a)
        level_stats = {
            level: {
                "count": len(lst),
                "accuracy": sum(1 for x in lst if x["correct"]) / len(lst)
            } for level, lst in by_level.items()
        }
        return {
            "total": total,
            "accuracy": acc,
            "avg_time": avg_t,
            "level_stats": level_stats
        }
