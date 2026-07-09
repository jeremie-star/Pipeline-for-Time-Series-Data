# Task 1 - EDA Summary

## Dataset understanding

- **Rows / columns:** 19,735 rows x 28 columns
- **Time range:** 2016-01-11 17:00:00 -> 2016-05-27 18:00:00 (137 days)
- **Frequency / granularity:** 0 days 00:10:00 (regular 10-minute sampling)
- **Total missing values:** 0 (dataset is complete; we still guard against gaps with time-ordered interpolation in preprocessing)
- **Target variable:** `Appliances` (appliance energy use, Wh)

## Statistical distribution of numerical columns

Saved to `outputs/describe.csv`. Target summary:

|       |   Appliances |
|:------|-------------:|
| count |    19735     |
| mean  |       97.695 |
| std   |      102.525 |
| min   |       10     |
| 25%   |       50     |
| 50%   |       60     |
| 75%   |      100     |
| max   |     1080     |


## Q2. Target distribution

- Appliances is strongly right-skewed (skewness = 3.39): most readings are low (10-100 Wh) with occasional high-usage spikes.

## Q3. Correlation with the target

Strongest correlations (|r|):

|        |       |r| |
|:-------|----------:|
| lights | 0.197278  |
| RH_out | 0.152282  |
| T2     | 0.120073  |
| T6     | 0.117638  |
| T_out  | 0.0991547 |


## Q4. Daily / weekly patterns

- Usage peaks around hour 18:00 (evening activity) and is lowest overnight; weekends differ from weekdays.

## Q5. Lag effect (LAG FEATURES)

Autocorrelation of Appliances with its own past:

|     |   autocorr |
|----:|-----------:|
|   1 |   0.753166 |
|   3 |   0.437789 |
|   6 |   0.323661 |
|  12 |   0.310939 |
| 144 |   0.216741 |

- Very strong at lag 1 (0.75) and still notable at 1 day (lag 144 = 0.22), which justifies the lag features used by the model.

## Q6. Moving averages (MOVING AVERAGES)

- The 1-hour moving average removes 10-minute noise while keeping the daily shape; the 1-day moving average exposes the slower trend. Both are engineered as model features.

## Q7. External weather variables

- Outdoor temperature correlates with energy use (r = 0.10); outdoor humidity and dew point also carry signal, so weather columns are kept as features.
