import os
import sys

import pandas as pd
import pymysql

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "outputs", "sql_results.md")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

QUERIES = {
    "Q1. Latest 5 records (latest-record query)":
        "SELECT reading_id, reading_ts, appliances_wh, lights_wh "
        "FROM reading ORDER BY reading_ts DESC LIMIT 5;",
    "Q2. Daily average for one week (date-range query)":
        "SELECT DATE(reading_ts) AS day, COUNT(*) AS n_readings, "
        "ROUND(AVG(appliances_wh),1) AS avg_appliances_wh, MAX(appliances_wh) AS peak_wh "
        "FROM reading WHERE reading_ts BETWEEN '2016-01-11' AND '2016-01-18' "
        "GROUP BY DATE(reading_ts) ORDER BY day;",
    "Q3. Hourly usage vs outdoor/indoor temperature (3-table join)":
        "SELECT HOUR(r.reading_ts) AS hour_of_day, ROUND(AVG(r.appliances_wh),1) AS avg_appliances_wh, "
        "ROUND(AVG(w.t_out),1) AS avg_outdoor_temp, ROUND(AVG(i.t2),1) AS avg_indoor_temp "
        "FROM reading r JOIN weather w ON w.reading_id=r.reading_id "
        "JOIN indoor_climate i ON i.reading_id=r.reading_id "
        "GROUP BY HOUR(r.reading_ts) ORDER BY hour_of_day;",
    "Q4. Top 10 high-usage events with indoor conditions":
        "SELECT r.reading_ts, r.appliances_wh, i.t2 AS living_temp, i.rh_1 AS kitchen_humidity "
        "FROM reading r JOIN indoor_climate i ON i.reading_id=r.reading_id "
        "ORDER BY r.appliances_wh DESC LIMIT 10;",
}


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Render a DataFrame as a GitHub-flavored markdown table without tabulate."""
    if df.empty:
        return "_No rows returned._"
    headers = [str(col) for col in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main():
    conn = pymysql.connect(**config.MYSQL)
    lines = ["# Task 2 - SQL query results\n",
             "Database `energy_ts` (tables: reading, indoor_climate, weather)\n"]
    for title, sql in QUERIES.items():
        df = pd.read_sql(sql, conn)
        lines += [f"## {title}\n", f"```sql\n{sql}\n```\n", dataframe_to_markdown(df), "\n"]
        print(f"  {title}: {len(df)} rows")
    with open(OUT, "w") as f:
        f.write("\n".join(lines))
    print(f"Saved -> {OUT}")
    conn.close()


if __name__ == "__main__":
    main()
