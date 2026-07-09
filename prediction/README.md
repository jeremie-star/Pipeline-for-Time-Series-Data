# Task 4 — Prediction / Forecast Script

**Owner: Jeremie Iyamurinze**

`predict.py` consolidates the whole pipeline end-to-end:

1. **Fetch** a window of recent records from the Task 3 API
   (`GET /mongo/readings/window`).
2. **Preprocess** them with the *same* `preprocessing.build_features` pipeline used
   in Task 1 (lag + moving-average + calendar + sensor features).
3. **Load** the trained model saved by the Task 1 notebook (`model.pkl`).
4. **Predict** the appliance energy use for the most recent record (one-step-ahead),
   and report accuracy across the fetched window.

## Run
```bash
# 1. Task 1 must have produced task1_eda_modeling/models/model.pkl
# 2. MongoDB must be loaded (task2_databases/load_mongo.py)
# 3. the API must be running (cd task3_api && uvicorn main:app)
python task4_prediction/predict.py
```

## Example output
```
[1/4] Fetching 300 recent records from http://127.0.0.1:8000/mongo/readings/window?n=300
[2/4] Preprocessing (lag + moving-average + calendar features)...
[3/4] Loading trained model from .../models/model.pkl
[4/4] Forecast for the latest record
  timestamp        : 2016-05-27 18:00:00
  PREDICTED usage  :   264.5 Wh
  actual usage     :   430.0 Wh  (a high-usage spike)
  mean abs. error over the 156-step window :   49.0 Wh
  model test RMSE (Task 1)                    : 58.14 Wh
```
