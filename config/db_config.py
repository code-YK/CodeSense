"""
Database configuration for CodeSense.
"""

import os
from dotenv import load_dotenv
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("CODESENSE_DB_HOST"),
    "port": int(os.getenv("CODESENSE_DB_PORT")),
    "dbname": os.getenv("CODESENSE_DB_NAME"),
    "user": os.getenv("CODESENSE_DB_USER"),
    "password": os.getenv("CODESENSE_DB_PASSWORD")
}

# Supported file extensions for code ingestion
SUPPORTED_EXTENSIONS = [".py", ".js"]

# Embedding model configuration
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
