# Time-Series Pipeline — Appliances Energy

End-to-end pipeline over the UCI Appliances Energy Prediction dataset: EDA and
forecasting, a MySQL and a MongoDB database, a REST API, and a prediction script.

Team (3): Jeremie Iyamurinze, Celine Shoga, Gentil Tonny Christian Iradukunda

## Dataset
Appliances Energy Prediction (UCI) — 19,735 readings at 10-minute granularity over
~4.5 months. Target: appliance energy use in Wh. Features: 9 indoor temperature and
9 humidity sensors plus outdoor weather. File: `data/raw/energydata_complete.csv`.

Goal: forecast short-term appliance energy use from recent usage (lag and
moving-average features) and environmental sensors.

## Layout
```
config.py                  shared paths + DB credentials (env-overridable)
data/raw/                  the dataset
task1_eda_modeling/        EDA, feature pipeline, model training (notebook)
task2_databases/           MySQL + MongoDB schema, loaders, queries
task3_api/                 FastAPI CRUD + time-series endpoints
task4_prediction/          fetch -> preprocess -> load model -> forecast
```

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# MySQL/MariaDB and MongoDB must be running locally
```

Create a MySQL/MariaDB user for the app (once), then point the project at it:
```bash
mysql <<'SQL'
CREATE DATABASE IF NOT EXISTS energy_ts;
CREATE USER IF NOT EXISTS 'energy'@'localhost' IDENTIFIED BY 'energy_pw';
GRANT ALL PRIVILEGES ON energy_ts.* TO 'energy'@'localhost';
FLUSH PRIVILEGES;
SQL

export MYSQL_USER=energy MYSQL_PASSWORD=energy_pw   # or edit config.py
```

## Run
```bash
# Task 1 — EDA + train model (writes task1_eda_modeling/models/model.pkl)
jupyter nbconvert --to notebook --execute --inplace \
    task1_eda_modeling/Task1_EDA_and_Modeling.ipynb

# Task 2 — load databases and run the queries
python task2_databases/load_sql.py    && python task2_databases/run_sql_queries.py
python task2_databases/load_mongo.py  && python task2_databases/run_mongo_queries.py

# Task 3 — start the API (Swagger UI at /docs, ReDoc at /redoc)
cd task3_api && uvicorn main:app --reload   # http://127.0.0.1:8000/docs
python task3_api/test_api.py                # smoke-test every endpoint (expect 21 passed)

# Task 4 — end-to-end forecast (API must be running)
python task4_prediction/predict.py
```

## What each task does
- Task 1 — Time-series EDA (7 analytical questions, incl. lag features and moving
  averages), a shared feature pipeline (`preprocessing.py`), and 3 model experiments
  with hyperparameter tuning. Best model: tuned Random Forest, test RMSE 58.14 Wh.
  Figures and tables in `task1_eda_modeling/outputs/`.
- Task 2 — MySQL schema (3 tables: `reading`, `indoor_climate`, `weather`) with ERD
  (`erd/erd.png`), MongoDB `readings` collection with sample documents, and query
  results in `task2_databases/outputs/`.
- Task 3 — FastAPI service with full CRUD plus latest-record and date-range endpoints
  over both MySQL and MongoDB.
- Task 4 — Script that fetches a window from the API, preprocesses it with the Task 1
  pipeline, loads `model.pkl`, and forecasts the latest record's usage.

## Requirements
Python 3.10+, a local MySQL server, and a local MongoDB server.
Exact packages are pinned in `requirements.txt`.
