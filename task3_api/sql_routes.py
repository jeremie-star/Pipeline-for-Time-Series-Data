"""CRUD and time-series endpoints backed by MySQL (energy_ts.reading).

Routes under /sql/readings:
  POST   /          create
  GET    /          list (limit/offset)
  GET    /latest    most recent reading
  GET    /range     readings in [start, end]
  GET    /{id}      read one
  PUT    /{id}      update (partial fields allowed)
  DELETE /{id}      delete
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pymysql.err import IntegrityError

from database import mysql_conn
from schemas import Message, ReadingIn, ReadingOut, ReadingUpdate

router = APIRouter(prefix="/sql/readings", tags=["SQL (MySQL)"])

_SELECT = "SELECT reading_id, reading_ts, appliances_wh, lights_wh FROM reading"


@router.post("", response_model=ReadingOut, status_code=201)
def create_reading(r: ReadingIn):
    try:
        with mysql_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO reading (reading_ts, appliances_wh, lights_wh) VALUES (%s, %s, %s)",
                (r.reading_ts, r.appliances_wh, r.lights_wh),
            )
            new_id = cur.lastrowid
    except IntegrityError:
        raise HTTPException(409, "A reading already exists for this timestamp")
    return {"reading_id": new_id, **r.model_dump()}


@router.get("", response_model=list[ReadingOut])
def list_readings(limit: int = Query(20, ge=1, le=500), offset: int = Query(0, ge=0)):
    with mysql_conn() as conn, conn.cursor() as cur:
        cur.execute(
            f"{_SELECT} ORDER BY reading_ts DESC LIMIT %s OFFSET %s",
            (limit, offset),
        )
        return cur.fetchall()


@router.get("/latest", response_model=ReadingOut)
def latest_reading():
    """Return the single most recent reading."""
    with mysql_conn() as conn, conn.cursor() as cur:
        cur.execute(f"{_SELECT} ORDER BY reading_ts DESC LIMIT 1")
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "No readings found")
    return row


@router.get("/range", response_model=list[ReadingOut])
def readings_by_range(
    start: datetime = Query(..., examples=["2016-01-11T17:00:00"]),
    end: datetime = Query(..., examples=["2016-01-11T20:00:00"]),
    limit: int = Query(500, ge=1, le=5000),
):
    """Return readings whose timestamp falls in [start, end]."""
    if end < start:
        raise HTTPException(422, "end must be greater than or equal to start")
    with mysql_conn() as conn, conn.cursor() as cur:
        cur.execute(
            f"{_SELECT} WHERE reading_ts BETWEEN %s AND %s ORDER BY reading_ts LIMIT %s",
            (start, end, limit),
        )
        return cur.fetchall()


@router.get("/{reading_id}", response_model=ReadingOut)
def get_reading(reading_id: int):
    with mysql_conn() as conn, conn.cursor() as cur:
        cur.execute(f"{_SELECT} WHERE reading_id = %s", (reading_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, f"reading {reading_id} not found")
    return row


@router.put("/{reading_id}", response_model=ReadingOut)
def update_reading(reading_id: int, r: ReadingUpdate):
    updates = r.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(422, "No fields provided to update")

    columns = ", ".join(f"{key} = %s" for key in updates)
    values = list(updates.values()) + [reading_id]
    with mysql_conn() as conn, conn.cursor() as cur:
        cur.execute(f"{_SELECT} WHERE reading_id = %s", (reading_id,))
        if cur.fetchone() is None:
            raise HTTPException(404, f"reading {reading_id} not found")
        try:
            cur.execute(f"UPDATE reading SET {columns} WHERE reading_id = %s", values)
        except IntegrityError:
            raise HTTPException(409, "A reading already exists for this timestamp")
        cur.execute(f"{_SELECT} WHERE reading_id = %s", (reading_id,))
        return cur.fetchone()


@router.delete("/{reading_id}", response_model=Message)
def delete_reading(reading_id: int):
    with mysql_conn() as conn, conn.cursor() as cur:
        n = cur.execute("DELETE FROM reading WHERE reading_id = %s", (reading_id,))
    if n == 0:
        raise HTTPException(404, f"reading {reading_id} not found")
    return {"detail": f"reading {reading_id} deleted"}
