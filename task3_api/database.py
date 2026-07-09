"""MySQL and MongoDB connection helpers for the API.

Credentials come from the shared project config.py.
"""

from __future__ import annotations

import os
import sys

import pymysql
from pymongo import ASCENDING, DESCENDING, MongoClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402


def mysql_conn():
    """Return a MySQL connection with a dict cursor and autocommit enabled."""
    return pymysql.connect(
        host=config.MYSQL["host"],
        port=config.MYSQL["port"],
        user=config.MYSQL["user"],
        password=config.MYSQL["password"],
        database=config.MYSQL["database"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


_mongo_client = MongoClient(config.MONGO["uri"], serverSelectionTimeoutMS=3000)
mongo_collection = _mongo_client[config.MONGO["database"]][config.MONGO["collection"]]
mongo_collection.create_index([("timestamp", DESCENDING)])
mongo_collection.create_index([("reading_id", ASCENDING)], unique=True)
