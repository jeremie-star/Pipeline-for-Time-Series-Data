-- =====================================================================
-- Task 2 - SQL queries on the energy_ts database
-- Author: Celine Shoga
-- Run:  mysql -u root -p energy_ts < queries.sql
-- (results are also captured programmatically by run_queries.py)
-- =====================================================================
USE energy_ts;

-- ---------------------------------------------------------------------
-- Query 1: LATEST RECORD (time-series requirement)
-- The 5 most recent readings, newest first.
-- ---------------------------------------------------------------------
SELECT reading_id, reading_ts, appliances_wh, lights_wh
FROM   reading
ORDER  BY reading_ts DESC
LIMIT  5;

-- ---------------------------------------------------------------------
-- Query 2: RECORDS BY DATE RANGE + daily aggregation (time-series req.)
-- Average appliance energy use per day for one week.
-- ---------------------------------------------------------------------
SELECT DATE(reading_ts)        AS day,
       COUNT(*)                AS n_readings,
       ROUND(AVG(appliances_wh), 1) AS avg_appliances_wh,
       MAX(appliances_wh)      AS peak_wh
FROM   reading
WHERE  reading_ts BETWEEN '2016-01-11' AND '2016-01-18'
GROUP  BY DATE(reading_ts)
ORDER  BY day;

-- ---------------------------------------------------------------------
-- Query 3: JOIN across all 3 tables - hourly usage vs outdoor temperature
-- Shows the evening peak and how usage relates to weather.
-- ---------------------------------------------------------------------
SELECT HOUR(r.reading_ts)          AS hour_of_day,
       ROUND(AVG(r.appliances_wh), 1) AS avg_appliances_wh,
       ROUND(AVG(w.t_out), 1)      AS avg_outdoor_temp,
       ROUND(AVG(i.t2), 1)         AS avg_indoor_temp
FROM   reading r
JOIN   weather        w ON w.reading_id = r.reading_id
JOIN   indoor_climate i ON i.reading_id = r.reading_id
GROUP  BY HOUR(r.reading_ts)
ORDER  BY hour_of_day;

-- ---------------------------------------------------------------------
-- Query 4: High-usage events - top 10 readings with indoor conditions
-- ---------------------------------------------------------------------
SELECT r.reading_ts, r.appliances_wh, i.t2 AS living_temp, i.rh_1 AS kitchen_humidity
FROM   reading r
JOIN   indoor_climate i ON i.reading_id = r.reading_id
ORDER  BY r.appliances_wh DESC
LIMIT  10;
