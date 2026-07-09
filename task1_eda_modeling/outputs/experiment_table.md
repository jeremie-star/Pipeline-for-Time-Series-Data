# Task 1C - Model Experiment Comparison

| Experiment                 |   RMSE |   MAE |     R2 | Notes                                                                                    |
|:---------------------------|-------:|------:|-------:|:-----------------------------------------------------------------------------------------|
| 1. Linear Regression       |  59.09 | 27.41 |  0.547 | baseline, scaled features                                                                |
| 2. Random Forest (default) | 110.41 | 78.08 | -0.581 | n_estimators=200, defaults                                                               |
| 3. Random Forest (tuned)   |  58.14 | 26.3  |  0.562 | best={'model__max_depth': 12, 'model__min_samples_leaf': 50, 'model__n_estimators': 300} |