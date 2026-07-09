# Task 2 - SQL query results

Database `energy_ts` (tables: reading, indoor_climate, weather)

## Q1. Latest 5 records (latest-record query)

```sql
SELECT reading_id, reading_ts, appliances_wh, lights_wh FROM reading ORDER BY reading_ts DESC LIMIT 5;
```

| reading_id | reading_ts | appliances_wh | lights_wh |
| --- | --- | --- | --- |
| 19735 | 2016-05-27 18:00:00 | 430 | 10 |
| 19734 | 2016-05-27 17:50:00 | 420 | 10 |
| 19733 | 2016-05-27 17:40:00 | 270 | 10 |
| 19732 | 2016-05-27 17:30:00 | 90 | 0 |
| 19731 | 2016-05-27 17:20:00 | 100 | 0 |


## Q2. Daily average for one week (date-range query)

```sql
SELECT DATE(reading_ts) AS day, COUNT(*) AS n_readings, ROUND(AVG(appliances_wh),1) AS avg_appliances_wh, MAX(appliances_wh) AS peak_wh FROM reading WHERE reading_ts BETWEEN '2016-01-11' AND '2016-01-18' GROUP BY DATE(reading_ts) ORDER BY day;
```

| day | n_readings | avg_appliances_wh | peak_wh |
| --- | --- | --- | --- |
| 2016-01-11 | 42 | 136.7 | 580 |
| 2016-01-12 | 144 | 85.7 | 500 |
| 2016-01-13 | 144 | 97.0 | 520 |
| 2016-01-14 | 144 | 151.4 | 910 |
| 2016-01-15 | 144 | 125.3 | 500 |
| 2016-01-16 | 144 | 125.3 | 1080 |
| 2016-01-17 | 144 | 142.7 | 800 |
| 2016-01-18 | 1 | 60.0 | 60 |


## Q3. Hourly usage vs outdoor/indoor temperature (3-table join)

```sql
SELECT HOUR(r.reading_ts) AS hour_of_day, ROUND(AVG(r.appliances_wh),1) AS avg_appliances_wh, ROUND(AVG(w.t_out),1) AS avg_outdoor_temp, ROUND(AVG(i.t2),1) AS avg_indoor_temp FROM reading r JOIN weather w ON w.reading_id=r.reading_id JOIN indoor_climate i ON i.reading_id=r.reading_id GROUP BY HOUR(r.reading_ts) ORDER BY hour_of_day;
```

| hour_of_day | avg_appliances_wh | avg_outdoor_temp | avg_indoor_temp |
| --- | --- | --- | --- |
| 0 | 52.8 | 6.1 | 20.1 |
| 1 | 51.3 | 5.8 | 19.8 |
| 2 | 49.1 | 5.6 | 19.6 |
| 3 | 48.2 | 5.3 | 19.4 |
| 4 | 49.4 | 5.0 | 19.2 |
| 5 | 52.7 | 4.9 | 19.1 |
| 6 | 57.7 | 4.8 | 19.0 |
| 7 | 78.6 | 5.0 | 19.0 |
| 8 | 106.1 | 5.6 | 19.4 |
| 9 | 112.8 | 6.6 | 20.1 |
| 10 | 125.4 | 7.6 | 20.7 |
| 11 | 133.1 | 8.6 | 21.0 |
| 12 | 123.6 | 9.3 | 21.2 |
| 13 | 124.7 | 9.8 | 21.2 |
| 14 | 108.3 | 10.2 | 21.2 |
| 15 | 105.8 | 10.4 | 21.2 |
| 16 | 119.9 | 10.3 | 21.2 |
| 17 | 161.4 | 10.0 | 21.0 |
| 18 | 190.4 | 9.4 | 20.9 |
| 19 | 143.1 | 8.8 | 20.9 |
| 20 | 127.0 | 8.1 | 20.9 |
| 21 | 96.5 | 7.4 | 20.9 |
| 22 | 69.1 | 6.8 | 20.7 |
| 23 | 57.0 | 6.4 | 20.4 |


## Q4. Top 10 high-usage events with indoor conditions

```sql
SELECT r.reading_ts, r.appliances_wh, i.t2 AS living_temp, i.rh_1 AS kitchen_humidity FROM reading r JOIN indoor_climate i ON i.reading_id=r.reading_id ORDER BY r.appliances_wh DESC LIMIT 10;
```

| reading_ts | appliances_wh | living_temp | kitchen_humidity |
| --- | --- | --- | --- |
| 2016-01-16 18:50:00 | 1080 | 21.04 | 42.7666666666667 |
| 2016-01-21 18:50:00 | 1070 | 18.4266666666667 | 34.3 |
| 2016-01-14 17:00:00 | 910 | 20.8566666666667 | 41.69333333333329 |
| 2016-04-04 15:40:00 | 900 | 22.2 | 43.16666666666671 |
| 2016-01-21 19:00:00 | 890 | 18.566666666666695 | 37.8633333333333 |
| 2016-03-25 19:00:00 | 880 | 20.8566666666667 | 40.53 |
| 2016-04-22 17:50:00 | 870 | 22.2675 | 37.59 |
| 2016-03-14 10:10:00 | 860 | 19.3266666666667 | 32.73 |
| 2016-01-24 08:30:00 | 850 | 16.9266666666667 | 44.16666666666671 |
| 2016-05-26 16:40:00 | 850 | 25.39 | 43.6266666666667 |

