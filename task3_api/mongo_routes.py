"""CRUD and time-series endpoints backed by MongoDB (energy_ts.readings).

Same resource shape as the SQL routes. Uses integer reading_id as the public id.

Routes under /mongo/readings:
  POST / | GET / | GET /latest | GET /range | GET /window | GET /{id} | PUT /{id} | DELETE /{id}
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.errors import DuplicateKeyError

from database import mongo_collection as col
from schemas import Message, ReadingIn, ReadingOut, ReadingUpdate

router = APIRouter(prefix="/mongo/readings", tags=["MongoDB"])

_WEATHER_MAP = {
    "t_out": "T_out",
    "press_mm_hg": "Press_mm_hg",
    "rh_out": "RH_out",
    "windspeed": "Windspeed",
    "visibility": "Visibility",
    "tdewpoint": "Tdewpoint",
}


def _out(doc: dict) -> dict:
    return {
        "reading_id": doc["reading_id"],
        "reading_ts": doc["timestamp"],
        "appliances_wh": doc["appliances_wh"],
        "lights_wh": doc["lights_wh"],
    }


def _next_reading_id() -> int:
    last = col.find_one(sort=[("reading_id", DESCENDING)], projection={"reading_id": 1})
    return (last["reading_id"] + 1) if last else 1


@router.post("", response_model=ReadingOut, status_code=201,
             summary="Create a reading", response_description="The created reading")
def create_reading(r: ReadingIn):
    """Insert a new document. Returns 409 if the id or timestamp already exists."""
    new_id = _next_reading_id()
    document = {
        "reading_id": new_id,
        "timestamp": r.reading_ts,
        "appliances_wh": r.appliances_wh,
        "lights_wh": r.lights_wh,
        "indoor": {},
        "weather": {},
    }
    try:
        col.insert_one(document)
    except DuplicateKeyError:
        raise HTTPException(409, "A reading already exists for this reading_id or timestamp")
    return {"reading_id": new_id, **r.model_dump()}


@router.get("", response_model=list[ReadingOut],
            summary="List readings", response_description="Readings, newest first")
def list_readings(limit: int = Query(20, ge=1, le=500), offset: int = Query(0, ge=0)):
    """List documents ordered by timestamp descending, with limit/offset paging."""
    cursor = col.find().sort("timestamp", DESCENDING).skip(offset).limit(limit)
    return [_out(doc) for doc in cursor]


@router.get("/latest", response_model=ReadingOut,
            summary="Latest record (time-series)",
            response_description="The most recent reading")
def latest_reading():
    """Time-series query: return the single most recent document by timestamp."""
    doc = col.find_one(sort=[("timestamp", DESCENDING)])
    if not doc:
        raise HTTPException(404, "No readings found")
    return _out(doc)


@router.get("/range", response_model=list[ReadingOut],
            summary="Records by date range (time-series)",
            response_description="Readings within [start, end]")
def readings_by_range(
    start: datetime = Query(..., examples=["2016-01-11T17:00:00"]),
    end: datetime = Query(..., examples=["2016-01-11T20:00:00"]),
    limit: int = Query(500, ge=1, le=5000),
):
    """Time-series query: documents whose timestamp falls in [start, end]."""
    if end < start:
        raise HTTPException(422, "end must be greater than or equal to start")
    cursor = (
        col.find({"timestamp": {"$gte": start, "$lte": end}})
        .sort("timestamp", ASCENDING)
        .limit(limit)
    )
    return [_out(doc) for doc in cursor]


@router.get("/window",
            summary="Recent full-record feed (for forecasting)",
            response_description="Raw-column records, oldest first")
def recent_window(n: int = Query(300, ge=1, le=2000)):
    """Return the n most recent full records (with sensors), oldest first.

    Used by the Task 4 forecast script to rebuild lag and moving-average features.
    Keys match the raw dataset columns so the shared preprocessing pipeline can
    consume them directly.
    """
    docs = list(col.find({}, {"_id": 0}).sort("timestamp", DESCENDING).limit(n))
    docs.reverse()
    rows = []
    for doc in docs:
        row = {
            "date": doc["timestamp"].isoformat(),
            "Appliances": doc["appliances_wh"],
            "lights": doc["lights_wh"],
        }
        row.update(doc.get("indoor", {}))
        row.update({_WEATHER_MAP[key]: value for key, value in doc.get("weather", {}).items() if key in _WEATHER_MAP})
        rows.append(row)
    return rows


@router.get("/{reading_id}", response_model=ReadingOut,
            summary="Get a reading by id", response_description="The requested reading")
def get_reading(reading_id: int):
    """Fetch one document by its reading_id. Returns 404 if not found."""
    doc = col.find_one({"reading_id": reading_id})
    if not doc:
        raise HTTPException(404, f"reading {reading_id} not found")
    return _out(doc)


@router.put("/{reading_id}", response_model=ReadingOut,
            summary="Update a reading", response_description="The updated reading")
def update_reading(reading_id: int, r: ReadingUpdate):
    """Partially update a document. Only the fields supplied are changed."""
    updates = r.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(422, "No fields provided to update")

    mongo_updates = {}
    if "reading_ts" in updates:
        mongo_updates["timestamp"] = updates["reading_ts"]
    if "appliances_wh" in updates:
        mongo_updates["appliances_wh"] = updates["appliances_wh"]
    if "lights_wh" in updates:
        mongo_updates["lights_wh"] = updates["lights_wh"]

    try:
        doc = col.find_one_and_update(
            {"reading_id": reading_id},
            {"$set": mongo_updates},
            return_document=ReturnDocument.AFTER,
        )
    except DuplicateKeyError:
        raise HTTPException(409, "A reading already exists for this timestamp")
    if doc is None:
        raise HTTPException(404, f"reading {reading_id} not found")
    return _out(doc)


@router.delete("/{reading_id}", response_model=Message,
               summary="Delete a reading", response_description="Deletion confirmation")
def delete_reading(reading_id: int):
    """Delete a document by reading_id. Returns 404 if it does not exist."""
    result = col.delete_one({"reading_id": reading_id})
    if result.deleted_count == 0:
        raise HTTPException(404, f"reading {reading_id} not found")
    return {"detail": f"reading {reading_id} deleted"}
