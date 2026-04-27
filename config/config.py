import os
from urllib.parse import quote_plus

DB_CONFIG = {
    "dbname": "sales_db",
    "user": "postgres",
    "password": "Mission@2026",
    "host": "10.20.80.49",
    "port": "5432"
}

password = quote_plus(DB_CONFIG["password"])

DB_URL = f"postgresql://{DB_CONFIG['user']}:{password}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
# This gives project root (sales-data-pipeline/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Paths
DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "pharma_sales_raw.csv")
RAW_FOLDER = os.path.join(DATA_DIR, "raw")
PROCESSED_FOLDER = os.path.join(DATA_DIR, "processed")

CHECKPOINT_FILE = os.path.join(DATA_DIR, "checkpoints", "last_processed.txt")

LOG_FILE = os.path.join(BASE_DIR, "logs", "pipeline.log")

