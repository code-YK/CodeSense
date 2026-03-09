"""
Database connection utilities for CodeSense.

Provides helpers to obtain a psycopg2 connection and to bootstrap the
database schema from the bundled SQL file.
"""

import os
import psycopg2

from config.db_config import DB_CONFIG


def get_connection():
    """Return a new psycopg2 connection using the project configuration."""
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    return conn


def initialize_database():
    """
    Read and execute database/schema.sql to set up the pgvector
    extension and create the required tables.
    """
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
        print("[✓] Database schema initialized successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[✗] Failed to initialize database: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
