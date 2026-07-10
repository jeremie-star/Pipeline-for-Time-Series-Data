import os
import sys

import pandas as pd
import pymysql

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

SCHEMA = os.path.join(os.path.dirname(__file__), "sql", "schema.sql")


def run_schema(cur):
    with open(SCHEMA) as f:
        lines = []
        for line in f:
            # Strip SQL line comments so semicolons inside comments do not
            # break statement splitting.
            code = line.split("--", 1)[0]
            lines.append(code)
        sql = "\n".join(lines)
    for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
        cur.execute(stmt)
    print("  schema created (energy_ts + reading, indoor_climate, weather)")


def main():
    df = pd.read_csv(config.RAW_CSV)
    df["date"] = pd.to_datetime(df["date"])
    df.insert(0, "reading_id", range(1, len(df) + 1))
    print(f"Loaded CSV: {len(df):,} rows")

    # connect without a database first so we can (re)create it
    conn = pymysql.connect(host=config.MYSQL["host"], port=config.MYSQL["port"],
                           user=config.MYSQL["user"], password=config.MYSQL["password"])
    cur = conn.cursor()
    run_schema(cur)
    conn.select_db("energy_ts")

    reading = list(df[["reading_id", "date", "Appliances", "lights"]].itertuples(index=False, name=None))
    cur.executemany(
        "INSERT INTO reading (reading_id, reading_ts, appliances_wh, lights_wh) VALUES (%s,%s,%s,%s)",
        reading)

    indoor_cols = ["reading_id", "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4",
                   "T5", "RH_5", "T6", "RH_6", "T7", "RH_7", "T8", "RH_8", "T9", "RH_9"]
    cur.executemany(
        "INSERT INTO indoor_climate VALUES (" + ",".join(["%s"] * len(indoor_cols)) + ")",
        list(df[indoor_cols].itertuples(index=False, name=None)))

    weather_cols = ["reading_id", "T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint"]
    cur.executemany(
        "INSERT INTO weather VALUES (" + ",".join(["%s"] * len(weather_cols)) + ")",
        list(df[weather_cols].itertuples(index=False, name=None)))

    conn.commit()
    for t in ("reading", "indoor_climate", "weather"):
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  {t}: {cur.fetchone()[0]:,} rows")
    cur.close(); conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
