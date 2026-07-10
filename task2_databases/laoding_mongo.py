import json
import os
import sys

import pandas as pd
from pymongo import ASCENDING, DESCENDING, MongoClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

INDOOR = [f"{p}{i}" for i in range(1, 10) for p in ("T", "RH_")]  # T1,RH_1,...,T9,RH_9
WEATHER = ["T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint"]
SAMPLE = os.path.join(os.path.dirname(__file__), "mongodb", "sample_documents.json")


def to_doc(row):
    return {
        "reading_id": int(row["reading_id"]),
        "timestamp": row["date"].to_pydatetime(),
        "appliances_wh": int(row["Appliances"]),
        "lights_wh": int(row["lights"]),
        "indoor": {c: float(row[c]) for c in INDOOR},
        "weather": {c.lower(): float(row[c]) for c in WEATHER},
    }


def main():
    df = pd.read_csv(config.RAW_CSV)
    df["date"] = pd.to_datetime(df["date"])
    df.insert(0, "reading_id", range(1, len(df) + 1))

    client = MongoClient(config.MONGO["uri"])
    col = client[config.MONGO["database"]][config.MONGO["collection"]]
    col.drop()

    docs = [to_doc(r) for _, r in df.iterrows()]
    col.insert_many(docs)
    col.create_index([("timestamp", DESCENDING)])
    col.create_index([("timestamp", ASCENDING)], unique=True)
    col.create_index([("reading_id", ASCENDING)], unique=True)
    print(f"Inserted {col.count_documents({}):,} documents into "
          f"{config.MONGO['database']}.{config.MONGO['collection']}")

    # save two clean sample documents for the report (drop the ObjectId _id)
    sample = [{k: v for k, v in d.items() if k != "_id"} for d in docs[:2]]
    for d in sample:
        d["timestamp"] = d["timestamp"].isoformat()
    with open(SAMPLE, "w") as f:
        json.dump(sample, f, indent=2)
    print(f"Wrote sample documents -> {SAMPLE}")
    client.close()


if __name__ == "__main__":
    main()
