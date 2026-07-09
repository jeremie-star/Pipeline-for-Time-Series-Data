# Task 1 — EDA, Feature Engineering & Modeling

**Owner: Jeremie Iyamurinze**

Time-series preprocessing, exploratory analysis, and forecasting of appliance
energy use (Wh) on the UCI Appliances Energy dataset.

## Contents
- **`Task1_EDA_and_Modeling.ipynb`** — the full deliverable (run top-to-bottom):
  dataset understanding, 7 analytical questions with plots + interpretation,
  feature engineering, and 3 model experiments with hyperparameter tuning.
- **`preprocessing.py`** — the shared feature pipeline (lag, moving-average,
  calendar, sensor features). Imported by the notebook **and** by the Task 4
  prediction script so preprocessing is identical everywhere.
- **`outputs/`** — exported figures, `eda_summary.md`, `experiment_table.md`.
- **`models/model.pkl`** — the trained best model (consumed by Task 4).

## Run
```bash
pip install -r ../requirements.txt
jupyter notebook Task1_EDA_and_Modeling.ipynb     # or: jupyter lab
# non-interactive:
jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=900 Task1_EDA_and_Modeling.ipynb
```

## Highlights
- **19,735** readings @ **10-minute** granularity over **137 days**, no missing values.
- Strong **daily seasonality**, evening peak (~18:00), heavily right-skewed target.
- **Lag features** (autocorrelation ≈ 0.75 at lag 1) and **moving averages** are the
  most important predictors — the two required feature types.

## Experiment results
| Experiment | RMSE | MAE | R² |
|---|---:|---:|---:|
| 1. Linear Regression (baseline) | 59.09 | 27.41 | 0.547 |
| 2. Random Forest (default) | 110.41 | 78.08 | −0.581 *(overfits)* |
| 3. **Random Forest (tuned)** | **58.14** | **26.30** | **0.562** |

Tuning regularisation hyperparameters (`max_depth`, `min_samples_leaf`) turns an
overfitting forest into the best model.
