"""
adaptive_engine.py

Simple rule-based adaptive logic.

Rules (configurable):
- Maintain current level unless performance over recent window shows trend.
- If accuracy over last N attempts >= up_inc_acc and avg_time <= time threshold -> increase difficulty.
- If accuracy over last N attempts <= down_dec_acc or avg_time > slow_time_threshold -> decrease difficulty.

Levels: ['easy', 'medium', 'hard']
"""

from typing import List
from tracker import Tracker

LEVELS = ["easy", "medium", "hard"]

class AdaptiveEngine:
    def __init__(self,
                 tracker: Tracker,
                 window: int = 5,
                 up_inc_acc: float = 0.8,
                 down_dec_acc: float = 0.5,
                 slow_time_threshold: float = 12.0):
        """
        tracker: Tracker instance
        window: how many recent attempts to consider
        up_inc_acc: accuracy threshold to go up
        down_dec_acc: accuracy threshold to go down
        slow_time_threshold: if avg time > threshold, treat as struggling
        """
        self.tracker = tracker
        self.window = window
        self.up_inc_acc = up_inc_acc
        self.down_dec_acc = down_dec_acc
        self.slow_time_threshold = slow_time_threshold

    def decide_next(self, current_level: str) -> str:
        """
        Decide next difficulty level given current_level.
        """
        if current_level not in LEVELS:
            current_level = "easy"

        recent_acc = self.tracker.accuracy(self.window)
        recent_time = self.tracker.average_time(self.window)

        # Debug lines (could be turned into logs)
        # print(f"[adaptive] recent_acc={recent_acc:.2f} recent_time={recent_time:.2f}")

        idx = LEVELS.index(current_level)

        # If doing well -> move up
        if recent_acc >= self.up_inc_acc and recent_time <= self.slow_time_threshold:
            next_idx = min(len(LEVELS) - 1, idx + 1)
            return LEVELS[next_idx]

        # If struggling -> move down
        if recent_acc <= self.down_dec_acc or recent_time > self.slow_time_threshold * 1.5:
            next_idx = max(0, idx - 1)
            return LEVELS[next_idx]

        # Otherwise, stay
        return current_level

    # Optional: placeholder to show how ML model could be plugged in later
    '''def ml_decide_next(self, current_level: str, model=None) -> str:
        """
        If you want to plug a trained lightweight ML model (e.g., logistic regression),
        use features like recent_acc, recent_time and predict probability for each level.
        This demo stub returns rule-based fallback.
        """
        # Implement ML logic here using model.predict(features) if provided
        return self.decide_next(current_level)'''
