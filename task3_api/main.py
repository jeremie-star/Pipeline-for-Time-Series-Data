"""FastAPI application for CRUD and time-series endpoints over MySQL and MongoDB.

Run from this folder:
    uvicorn main:app --reload

Interactive docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

import mongo_routes
import sql_routes

tags_metadata = [
    {
        "name": "SQL (MySQL)",
        "description": "CRUD plus latest-record and date-range queries over the "
        "relational `energy_ts.reading` table.",
    },
    {
        "name": "MongoDB",
        "description": "The same CRUD and time-series operations over the "
        "`energy_ts.readings` collection, plus a `/window` feed used by the "
        "Task 4 forecast script.",
    },
    {"name": "health", "description": "Service and liveness checks."},
]

app = FastAPI(
    title="Time-Series Energy API",
    summary="CRUD and time-series endpoints for the Appliances Energy dataset.",
    description=(
        "A single API exposing symmetric endpoints over **two** databases "
        "(MySQL and MongoDB) for the UCI Appliances Energy time series.\n\n"
        "Each backend supports full CRUD (POST / GET / PUT / DELETE) plus the two "
        "required time-series queries:\n\n"
        "- **Latest record** — `GET /{sql|mongo}/readings/latest`\n"
        "- **Records by date range** — `GET /{sql|mongo}/readings/range?start=&end=`\n\n"
        "Interactive docs: **Swagger UI** at `/docs`, **ReDoc** at `/redoc`, "
        "raw schema at `/openapi.json`."
    ),
    version="1.0.0",
    contact={"name": "Time-Series Pipeline Team"},
    license_info={"name": "MIT"},
    openapi_tags=tags_metadata,
)

app.include_router(sql_routes.router)
app.include_router(mongo_routes.router)


@app.get("/", tags=["health"])
def root():
    return {
        "service": "Time-Series Energy API",
        "status": "ok",
        "databases": ["mysql:energy_ts.reading", "mongodb:energy_ts.readings"],
        "docs": "/docs",
        "endpoints": {
            "sql": "/sql/readings [POST,GET,PUT,DELETE] + /latest + /range",
            "mongo": "/mongo/readings [POST,GET,PUT,DELETE] + /latest + /range + /window",
        },
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
