# Building a Pipeline for Time-Series Data

An end-to-end pipeline over the **UCI Appliances Energy Prediction** time-series
dataset: exploratory analysis and forecasting, relational + document databases,
a REST API, and a consolidated prediction script.

> **Course:** Formative 1 — Building a Pipeline for Time Series Data
> **Team (3):** Jeremie Iyamurinze · Celine Shoga · Gentil Tonny Christian Iradukunda

## Dataset
**Appliances Energy Prediction** (UCI) — 19,735 readings at **10-minute** granularity
over ~4.5 months. Each reading has the target **appliance energy use (Wh)** plus
9 indoor temperature + 9 humidity sensors and outdoor weather.
`data/raw/energydata_complete.csv`.

**Problem:** forecast short-term appliance energy use from recent usage history
(lag / moving-average features) and environmental sensors — useful for demand
awareness and load management.

## Repository structure
```
.
├── config.py                     # shared paths + DB credentials (env-overridable)
├── requirements.txt
├── data/
│   └── energydata_complete.csv
├── eda_modeling/           # Task 1  (Jeremie)  — EDA, features, model  [notebook]
├── databases/              # Task 2  (Celine)   — MySQL + MongoDB + ERD
├── api/                    # Task 3  (Gentil)   — FastAPI CRUD + time-series endpoints
├── prediction/             # Task 4  (Jeremie)  — end-to-end forecast script
└── report/                       # PDF report source
```

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# databases (MySQL + MongoDB must be running locally)
export MYSQL_PASSWORD='your_password'      # or edit config.py
```

## Run the whole pipeline
```bash
# Task 1 - EDA + train model (creates models/model.pkl)
jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=900 \
    task1_eda_modeling/Task1_EDA_and_Modeling.ipynb

# Task 2 - build + load databases, run queries
python task2_databases/load_sql.py    && python task2_databases/run_sql_queries.py
python task2_databases/load_mongo.py  && python task2_databases/run_mongo_queries.py

# Task 3 - start the API
( cd task3_api && uvicorn main:app --reload )      # http://127.0.0.1:8000/docs
python task3_api/test_api.py                        # smoke-test all endpoints

# Task 4 - end-to-end forecast (API must be running)
python task4_prediction/predict.py
```

## Tasks at a glance
| Task | What | Owner | Folder |
|---|---|---|---|
| 1 | Time-series EDA, feature engineering, model + tuning | Jeremie | `task1_eda_modeling/` |
| 2 | MySQL schema + ERD, MongoDB design, queries | Celine | `task2_databases/` |
| 3 | FastAPI CRUD + latest/date-range endpoints (SQL & Mongo) | Gentil | `task3_api/` |
| 4 | Fetch → preprocess → load model → forecast | Jeremie | `task4_prediction/` |

See each task folder's `README.md` for details, and `report/report.md` for the
full write-up and per-member contributions.

## Requirements
- Python 3.10+
- MySQL server (running locally)
- MongoDB server (running locally)
