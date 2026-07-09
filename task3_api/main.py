"""FastAPI application for CRUD and time-series endpoints over MySQL and MongoDB.

Run from this folder:
    uvicorn main:app --reload

Interactive docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

import mongo_routes
import sql_routes

app = FastAPI(
    title="Time-Series Energy API",
    description=(
        "CRUD, latest-record, and date-range endpoints over MySQL and MongoDB "
        "for the Appliances Energy dataset."
    ),
    version="1.0.0",
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
