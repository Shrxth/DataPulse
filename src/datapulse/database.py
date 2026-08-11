from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DEFAULT_DB_PATH = Path("database") / "datapulse.db"


CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS earthquakes (
    event_id TEXT PRIMARY KEY,
    event_time TEXT NOT NULL,
    magnitude REAL NOT NULL,
    place TEXT NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    depth_km REAL NOT NULL,
    event_url TEXT,
    event_type TEXT,
    magnitude_category TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_hour INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def initialize_database(db_path: Path = DEFAULT_DB_PATH) -> None:
    """Create the DataPulse database schema if it does not exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        connection.execute(CREATE_EVENTS_TABLE)
        connection.commit()


def insert_earthquakes(
    df: pd.DataFrame,
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Insert new earthquake events and ignore already-known event IDs."""
    initialize_database(db_path)

    records = [
        (
            row.event_id,
            row.event_time.isoformat(),
            float(row.magnitude),
            row.place,
            float(row.longitude),
            float(row.latitude),
            float(row.depth_km),
            row.event_url,
            row.event_type,
            str(row.magnitude_category),
            str(row.event_date),
            int(row.event_hour),
        )
        for row in df.itertuples(index=False)
    ]

    if not records:
        return 0

    with sqlite3.connect(db_path) as connection:
        cursor = connection.executemany(
            """
            INSERT OR IGNORE INTO earthquakes (
                event_id,
                event_time,
                magnitude,
                place,
                longitude,
                latitude,
                depth_km,
                event_url,
                event_type,
                magnitude_category,
                event_date,
                event_hour
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            records,
        )
        connection.commit()

    return cursor.rowcount


def get_event_count(
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Return the total number of stored earthquake events."""
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM earthquakes"
        ).fetchone()

    return int(result[0])


def query_earthquakes(
    query: str,
    db_path: Path = DEFAULT_DB_PATH,
) -> pd.DataFrame:
    """Execute a read-only analytical SQL query."""
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)


def get_daily_event_counts(
    db_path: Path = DEFAULT_DB_PATH,
) -> pd.DataFrame:
    """Return historical daily earthquake counts from SQLite."""
    initialize_database(db_path)

    query = """
        SELECT
            event_date,
            COUNT(*) AS event_count
        FROM earthquakes
        GROUP BY event_date
        ORDER BY event_date
    """

    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)