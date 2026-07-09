"""Shared preprocessing pipeline for the Appliances Energy time series.

This module is the single source of truth for how raw sensor rows are turned
into model-ready features. It is imported by:
  * train.py            (Task 1 - model training)
  * ../task4_prediction/predict.py (Task 4 - forecasting on a fetched record)

Keeping the logic here guarantees the prediction script preprocesses data
*exactly* the way the model was trained.

Author: Jeremie Iyamurinze
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

TARGET = "Appliances"

# Sensor / weather columns kept as-is (the value at time t).
# rv1 and rv2 are documented in the dataset as random noise variables, so we drop them.
SENSOR_COLS = [
    "lights",
    "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4", "T5", "RH_5",
    "T6", "RH_6", "T7", "RH_7", "T8", "RH_8", "T9", "RH_9",
    "T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint",
]

# Data is sampled every 10 minutes -> 6 steps = 1 hour, 144 steps = 1 day.
LAGS = [1, 2, 3, 6, 144]          # 10min, 20min, 30min, 1h, 1day ago
ROLL_WINDOWS = [6, 144]           # 1-hour and 1-day moving averages


def load_raw(path=None):
    """Load the raw CSV and parse the timestamp into a DatetimeIndex."""
    path = path or config.RAW_CSV
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").set_index("date")
    return df


def add_time_features(df):
    """Calendar features that capture daily / weekly seasonality."""
    idx = df.index
    df["hour"] = idx.hour
    df["dayofweek"] = idx.dayofweek
    df["month"] = idx.month
    df["is_weekend"] = (idx.dayofweek >= 5).astype(int)
    return df


def add_lag_features(df, target=TARGET, lags=LAGS):
    """Past values of the target (answers 'do previous readings predict now?')."""
    for lag in lags:
        df[f"{target}_lag_{lag}"] = df[target].shift(lag)
    return df


def add_rolling_features(df, target=TARGET, windows=ROLL_WINDOWS):
    """Moving averages / std of the target, shifted by 1 to avoid leaking the present."""
    for w in windows:
        df[f"{target}_roll_mean_{w}"] = df[target].shift(1).rolling(w).mean()
        df[f"{target}_roll_std_{w}"] = df[target].shift(1).rolling(w).std()
    return df


def build_features(df):
    """Full pipeline: raw sensor frame -> (feature matrix X, target y).

    Rows containing NaNs created by the lag/rolling windows are dropped.
    Returns X, y and the ordered list of feature column names.
    """
    df = df.copy()
    df = add_time_features(df)
    df = add_lag_features(df)
    df = add_rolling_features(df)
    df = df.dropna()

    feature_cols = (
        SENSOR_COLS
        + ["hour", "dayofweek", "month", "is_weekend"]
        + [f"{TARGET}_lag_{l}" for l in LAGS]
        + [f"{TARGET}_roll_mean_{w}" for w in ROLL_WINDOWS]
        + [f"{TARGET}_roll_std_{w}" for w in ROLL_WINDOWS]
    )
    X = df[feature_cols]
    y = df[TARGET]
    return X, y, feature_cols


def chronological_split(X, y, test_frac=0.2):
    """Split keeping time order (no shuffling) - the correct way for forecasting."""
    n_test = int(len(X) * test_frac)
    return (
        X.iloc[:-n_test], X.iloc[-n_test:],
        y.iloc[:-n_test], y.iloc[-n_test:],
    )
