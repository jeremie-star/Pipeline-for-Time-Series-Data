"""Shared configuration for the Time-Series Pipeline project.

Central place for file paths and database credentials so every task
(EDA/modeling, databases, API, prediction) uses the same settings.
Override any value with an environment variable of the same name.
"""
import os

# paths
ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_CSV = os.path.join(ROOT, "data", "raw", "energydata_complete.csv")
PROCESSED_CSV = os.path.join(ROOT, "data", "processed", "features.csv")
MODEL_PATH = os.path.join(ROOT, "task1_eda_modeling", "models", "model.pkl")

# MySQL
MYSQL = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "energy_ts"),
}

# MongoDB
MONGO = {
    "uri": os.getenv("MONGO_URI", "mongodb://localhost:27017"),
    "database": os.getenv("MONGO_DB", "energy_ts"),
    "collection": os.getenv("MONGO_COLLECTION", "readings"),
}

# API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
