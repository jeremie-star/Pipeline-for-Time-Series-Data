"""Task 4 - End-to-end forecast script.

Consolidates the whole pipeline:
  1. FETCH   a window of recent time-series records from the Task 3 API
  2. PREPROCESS them with the *same* pipeline used in Task 1 (preprocessing.build_features)
  3. LOAD    the trained model saved by the Task 1 notebook (model.pkl)
  4. PREDICT the appliance energy use for the most recent record (one-step-ahead)

Run (API must be running - see task3_api/README.md):
    python task4_prediction/predict.py

Author: Jeremie Iyamurinze
"""
import os
import sys

import joblib
import pandas as pd
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT, "task1_eda_modeling"))  # reuse the Task 1 pipeline
import config  # noqa: E402
from preprocessing import build_features  # noqa: E402


def fetch_window(n=300):
    """Step 1 - fetch the last `n` full records from the API."""
    url = f"{config.API_BASE_URL}/mongo/readings/window?n={n}"
    print(f"[1/4] Fetching {n} recent records from {url}")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    rows = resp.json()
    print(f"      got {len(rows)} records "
          f"({rows[0]['date']} -> {rows[-1]['date']})")
    return rows


def main():
    #  1. fetch
    rows = fetch_window(n=300)
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").set_index("date")

    #  2. preprocess (same as Task 1)
    print("[2/4] Preprocessing (lag + moving-average + calendar features)...")
    X, y, feature_cols = build_features(df)
    if X.empty:
        raise SystemExit("Not enough history to build features - request a larger window.")

    #  3. load model
    print(f"[3/4] Loading trained model from {config.MODEL_PATH}")
    # model.pkl is our own artifact produced locally by the Task 1 notebook (trusted).
    bundle = joblib.load(config.MODEL_PATH)
    pipeline, cols = bundle["pipeline"], bundle["feature_cols"]
    X = X.reindex(columns=cols)  # guarantee identical column order

    #  4. predict latest
    latest_ts = X.index[-1]
    x_latest = X.iloc[[-1]]
    y_pred = float(pipeline.predict(x_latest)[0])
    y_actual = float(y.iloc[-1])

    print("[4/4] Forecast for the latest record")
    print("-" * 48)
    print(f"  timestamp        : {latest_ts}")
    print(f"  predicted usage  : {y_pred:7.1f} Wh")
    print(f"  actual usage     : {y_actual:7.1f} Wh")
    print(f"  absolute error   : {abs(y_pred - y_actual):7.1f} Wh")
    print(f"  model test RMSE  : {bundle['metrics']['RMSE']} Wh (from Task 1)")
    print("-" * 48)
    print("Pipeline complete: API -> preprocess -> model -> prediction.")


if __name__ == "__main__":
    main()
