-- =====================================================================
-- Task 2 - Relational schema for the Appliances Energy time series
-- Author: Celine Shoga
-- Database: MySQL
--
-- Design (3 tables, normalized around the timestamp):
--   reading         -> central time-series FACT (the target: appliance energy)
--   indoor_climate  -> indoor temp/humidity sensors  (1:1 with reading)
--   weather         -> outdoor weather conditions     (1:1 with reading)
-- reading_id is the shared key; reading_ts is indexed for fast
-- "latest record" and "date range" time-series queries.
-- =====================================================================

DROP DATABASE IF EXISTS energy_ts;
CREATE DATABASE energy_ts;
USE energy_ts;

-- --------------------------------------------------------------- FACT
CREATE TABLE reading (
    reading_id    INT AUTO_INCREMENT PRIMARY KEY,  -- API POSTs get a fresh id
    reading_ts    DATETIME    NOT NULL,
    appliances_wh INT         NOT NULL,   -- target variable (Wh)
    lights_wh     INT         NOT NULL,
    UNIQUE KEY uq_reading_ts (reading_ts),
    INDEX idx_reading_ts (reading_ts)
);

-- ------------------------------------------------------ indoor sensors
CREATE TABLE indoor_climate (
    reading_id INT PRIMARY KEY,
    t1  DOUBLE, rh_1 DOUBLE,
    t2  DOUBLE, rh_2 DOUBLE,
    t3  DOUBLE, rh_3 DOUBLE,
    t4  DOUBLE, rh_4 DOUBLE,
    t5  DOUBLE, rh_5 DOUBLE,
    t6  DOUBLE, rh_6 DOUBLE,
    t7  DOUBLE, rh_7 DOUBLE,
    t8  DOUBLE, rh_8 DOUBLE,
    t9  DOUBLE, rh_9 DOUBLE,
    CONSTRAINT fk_indoor_reading FOREIGN KEY (reading_id)
        REFERENCES reading (reading_id) ON DELETE CASCADE
);

-- ----------------------------------------------------- outdoor weather
CREATE TABLE weather (
    reading_id  INT PRIMARY KEY,
    t_out       DOUBLE,
    press_mm_hg DOUBLE,
    rh_out      DOUBLE,
    windspeed   DOUBLE,
    visibility  DOUBLE,
    tdewpoint   DOUBLE,
    CONSTRAINT fk_weather_reading FOREIGN KEY (reading_id)
        REFERENCES reading (reading_id) ON DELETE CASCADE
);
