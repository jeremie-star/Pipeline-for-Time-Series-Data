# Task 2 — Databases (SQL + MongoDB)

**Owner: Celine Shoga**

Two implementations of the same Appliances Energy time series: a normalised
**MySQL** schema and a document-oriented **MongoDB** collection.

## Contents
```
task2_databases/
├── sql/
│   ├── schema.sql        # 3-table relational schema (reading, indoor_climate, weather)
│   └── queries.sql       # the 4 SQL queries
├── mongodb/
│   ├── design.md         # collection design rationale
│   └── sample_documents.json
├── erd/
│   ├── erd.md            # Mermaid ERD (renders on GitHub)
│   ├── erd.png           # rendered image for the report
│   └── build_erd.py
├── load_sql.py           # create schema + load CSV into MySQL
├── load_mongo.py         # load CSV into MongoDB
├── run_sql_queries.py    # run the 4 SQL queries -> outputs/sql_results.md
├── run_mongo_queries.py  # run the 4 Mongo queries -> outputs/mongo_results.md
└── outputs/              # captured query results
```

## Relational design (3 tables)
`reading` is the central **fact** table holding the target (appliance energy).
Each reading has one `indoor_climate` row (9 temp + 9 humidity sensors) and one
`weather` row (outdoor conditions), linked 1:1 by `reading_id`. `reading_ts` is
unique and indexed for fast latest/date-range queries. See `erd/erd.png`.

## MongoDB design
One `readings` collection, one document per timestamp, with `indoor` and `weather`
nested sub-documents and an index on `timestamp`. See `mongodb/design.md`.

## How to run
```bash
# from the repo root, with the virtualenv active
export MYSQL_PASSWORD='your_password'        # or edit config.py

python task2_databases/load_sql.py           # build + load MySQL
python task2_databases/run_sql_queries.py    # -> outputs/sql_results.md

python task2_databases/load_mongo.py         # build + load MongoDB
python task2_databases/run_mongo_queries.py  # -> outputs/mongo_results.md
```

## Required queries (both databases)
1. **Latest record** (time-series requirement)
2. **Records by date range** + daily aggregation (time-series requirement)
3. Hourly usage vs temperature (SQL: 3-table join / Mongo: `$group` aggregation)
4. High-usage events

Results are captured in `outputs/sql_results.md` and `outputs/mongo_results.md`.
