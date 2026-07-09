# MongoDB Collection Design — `energy_ts.readings`

**Author: Celine Shoga**

## Why a document model here
The relational design splits one timestamp across three tables (`reading`,
`indoor_climate`, `weather`) to avoid a very wide table. In MongoDB we take the
opposite, read-optimised approach: **one document per timestamp**, with the indoor
and outdoor sensors nested as sub-documents. A single query then returns the whole
observation with no joins — ideal for serving time-series records to the API and
the prediction script.

## Collection: `readings`
- One document = one 10-minute observation.
- `timestamp` is stored as a real `Date` (BSON), so range and `$hour` aggregation
  queries work natively.
- An **index on `timestamp` (descending)** makes "latest record" and
  "date range" queries fast — the two required time-series endpoints.

## Document shape
```json
{
  "reading_id": 1,
  "timestamp": ISODate("2016-01-11T17:00:00Z"),
  "appliances_wh": 60,
  "lights_wh": 30,
  "indoor": {
    "T1": 19.89, "RH_1": 47.60,
    "T2": 19.20, "RH_2": 44.79,
    "T3": 19.79, "RH_3": 44.73,
    "T4": 19.00, "RH_4": 45.57,
    "T5": 17.17, "RH_5": 55.20,
    "T6": 7.03,  "RH_6": 84.26,
    "T7": 17.20, "RH_7": 41.63,
    "T8": 18.20, "RH_8": 48.90,
    "T9": 17.03, "RH_9": 45.53
  },
  "weather": {
    "t_out": 6.60, "press_mm_hg": 733.5, "rh_out": 92.0,
    "windspeed": 7.0, "visibility": 63.0, "tdewpoint": 5.3
  }
}
```

## Indexes
```js
db.readings.createIndex({ timestamp: -1 })   // latest record + date range
db.readings.createIndex({ reading_id: 1 }, { unique: true })
```

See `sample_documents.json` for real example documents and `../run_mongo_queries.py`
for the three required queries and their results.
