# Task 3 — API (CRUD + Time-Series Endpoints)

**Owner: Gentil Tonny Christian Iradukunda**

FastAPI service exposing full CRUD plus the required time-series queries
(**latest record**, **date range**) for **both** MySQL and MongoDB from Task 2.

## Run

```bash
# databases from Task 2 must be loaded first
export MYSQL_PASSWORD='your_password'   # only if MySQL root/user needs a password
cd task3_api
uvicorn main:app --reload
# interactive docs: http://127.0.0.1:8000/docs
```

## Endpoints

| Method | SQL path | Mongo path | Purpose |
|--------|----------|------------|---------|
| POST   | `/sql/readings`        | `/mongo/readings`        | Create |
| GET    | `/sql/readings`        | `/mongo/readings`        | List (limit/offset) |
| GET    | `/sql/readings/latest` | `/mongo/readings/latest` | Latest record |
| GET    | `/sql/readings/range`  | `/mongo/readings/range`  | Records by date range |
| GET    | `/sql/readings/{id}`   | `/mongo/readings/{id}`   | Read one |
| PUT    | `/sql/readings/{id}`   | `/mongo/readings/{id}`   | Update |
| DELETE | `/sql/readings/{id}`   | `/mongo/readings/{id}`   | Delete |
| GET    | —                      | `/mongo/readings/window` | Recent full records (Task 4) |

## Example

```bash
curl http://127.0.0.1:8000/sql/readings/latest
curl "http://127.0.0.1:8000/mongo/readings/range?start=2016-01-11T17:00:00&end=2016-01-11T18:00:00"
curl -X POST http://127.0.0.1:8000/sql/readings \
     -H "Content-Type: application/json" \
     -d '{"reading_ts":"2016-05-27T18:10:00","appliances_wh":60,"lights_wh":10}'
```

## Smoke test

```bash
python task3_api/test_api.py
```

## Files

- `main.py` — app and router registration
- `database.py` — MySQL (PyMySQL) and MongoDB (pymongo) connections
- `schemas.py` — Pydantic request/response models
- `sql_routes.py` — MySQL CRUD + latest + range
- `mongo_routes.py` — MongoDB CRUD + latest + range + window
- `test_api.py` — smoke test for every endpoint on both databases
