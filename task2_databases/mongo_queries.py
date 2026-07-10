import os
import sys

from pymongo import DESCENDING, MongoClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "outputs", "mongo_results.md")
os.makedirs(os.path.dirname(OUT), exist_ok=True)


def main():
    client = MongoClient(config.MONGO["uri"])
    col = client[config.MONGO["database"]][config.MONGO["collection"]]
    lines = ["# Task 2 - MongoDB query results\n",
             f"Collection `{config.MONGO['database']}.{config.MONGO['collection']}` "
             f"({col.count_documents({}):,} documents)\n"]

    # Q1 latest record
    lines.append("## Q1. Latest record\n```js\ndb.readings.find().sort({timestamp:-1}).limit(1)\n```")
    doc = col.find_one(sort=[("timestamp", DESCENDING)], projection={"_id": 0, "indoor": 0})
    lines.append(f"Result: `{doc}`\n")

    # Q2 date range
    import datetime as dt
    start, end = dt.datetime(2016, 1, 11), dt.datetime(2016, 1, 12)
    lines.append("## Q2. Records in a date range (2016-01-11)\n"
                 "```js\ndb.readings.find({timestamp:{$gte:ISODate('2016-01-11'),"
                 "$lt:ISODate('2016-01-12')}})\n```")
    n = col.count_documents({"timestamp": {"$gte": start, "$lt": end}})
    first3 = list(col.find({"timestamp": {"$gte": start, "$lt": end}},
                           {"_id": 0, "timestamp": 1, "appliances_wh": 1}).limit(3))
    lines.append(f"Matched {n} readings. First 3: `{first3}`\n")

    # Q3 aggregation by hour
    lines.append("## Q3. Average appliance usage by hour of day (aggregation)\n"
                 "```js\ndb.readings.aggregate([{$group:{_id:{$hour:'$timestamp'},"
                 "avg:{$avg:'$appliances_wh'}}},{$sort:{_id:1}}])\n```")
    agg = list(col.aggregate([
        {"$group": {"_id": {"$hour": "$timestamp"}, "avg_wh": {"$avg": "$appliances_wh"}}},
        {"$sort": {"_id": 1}}]))
    lines.append("| hour | avg_appliances_wh |\n|---:|---:|")
    for a in agg:
        lines.append(f"| {a['_id']} | {a['avg_wh']:.1f} |")
    lines.append("")

    # Q4 high usage
    lines.append("## Q4. High-usage events (> 600 Wh)\n"
                 "```js\ndb.readings.find({appliances_wh:{$gt:600}}).sort({appliances_wh:-1}).limit(5)\n```")
    hi = list(col.find({"appliances_wh": {"$gt": 600}},
                       {"_id": 0, "timestamp": 1, "appliances_wh": 1})
              .sort("appliances_wh", DESCENDING).limit(5))
    lines.append(f"Top 5: `{hi}`\n")

    with open(OUT, "w") as f:
        f.write("\n".join(str(x) for x in lines))
    print(f"Saved -> {OUT}")
    client.close()


if __name__ == "__main__":
    main()
