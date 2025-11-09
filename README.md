README.md
# Math Adventures — AI-Powered Adaptive Learning Prototype

## Overview
Small adaptive math practice prototype for children (ages 5–10). Demonstrates an adaptive engine that adjusts puzzle difficulty (Easy / Medium / Hard) based on recent performance (accuracy and response time).

This is a console demo. Code is modular and ready for extension into a web or Streamlit app.

## How to run
1. Clone the repo:


git clone https://github.com/AnishShaw1/MATH-ADAPTIVE-PROTOTYPE
cd math-adaptive-prototype

2. (Optional) Create virtualenv and install requirements:


python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Run:


python src/main.py


## Files
- `src/puzzle_generator.py` — creates puzzles per difficulty
- `src/tracker.py` — logs attempts & computes metrics
- `src/adaptive_engine.py` — rule-based logic that decides next difficulty
- `src/main.py` — console UI for demo
- `TECHNICAL_NOTE.md` — short 1–2 page technical note (architecture, reasoning)

## Notes / Future work
- Swap in a lightweight ML model (logistic regression) in `AdaptiveEngine.ml_decide_next`.
- Extend to Streamlit interface (simple) or mobile/teacher dashboard for analytics.
- Store session logs to a CSV/DB for training improved models.
