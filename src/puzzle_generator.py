"""
puzzle_generator.py

Generates math puzzles for three difficulty levels:
- Easy: addition/subtraction, small numbers
- Medium: include multiplication, larger numbers
- Hard: include division (integer results), bigger numbers
"""

import random
from typing import Tuple

OPS = ["+", "-", "*", "/"]

def generate_puzzle(difficulty: str) -> Tuple[str, float]:
    """
    Return a tuple (question_str, correct_answer)
    difficulty: 'easy' | 'medium' | 'hard'
    """

    if difficulty == "easy":
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        op = random.choice(["+", "-"])
    elif difficulty == "medium":
        a = random.randint(0, 20)
        b = random.randint(0, 12)
        op = random.choice(["+", "-", "*"])
    elif difficulty == "hard":
        # make division produce integer answers sometimes
        op = random.choice(["+", "-", "*", "/"])
        if op == "/":
            b = random.randint(1, 12)
            ans = random.randint(1, 12)
            a = b * ans
        else:
            a = random.randint(0, 100)
            b = random.randint(1, 50)
    else:
        raise ValueError("Unknown difficulty")

    # compute answer
    if op == "+":
        ans = a + b
    elif op == "-":
        ans = a - b
    elif op == "*":
        ans = a * b
    elif op == "/":
        # avoid zero division and give float answer (but often integer)
        ans = a / b
    else:
        raise ValueError("Bad op")

    q = f"{a} {op} {b} = ?"
    return q, ans
