from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "medisub.db"
DB_PATH_ENV_VAR = "MEDISUB_DB_PATH"

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS question_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    predicted_category TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at TEXT NOT NULL
)
"""


def resolve_db_path(db_path: str | Path | None = None) -> Path:
    configured_path = db_path or os.getenv(DB_PATH_ENV_VAR) or DEFAULT_DB_PATH
    return Path(configured_path).expanduser().resolve()


def initialize_database(db_path: str | Path | None = None) -> Path:
    path = resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute(_CREATE_TABLE_SQL)
    return path


def save_question_event(
    question: str,
    predicted_category: str,
    confidence: float,
    *,
    db_path: str | Path | None = None,
    created_at: str | None = None,
) -> int:
    timestamp = created_at or datetime.now(timezone.utc).isoformat()
    path = initialize_database(db_path)
    with sqlite3.connect(path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO question_events (question, predicted_category, confidence, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (question, predicted_category, float(confidence), timestamp),
        )
        return int(cursor.lastrowid)


def list_question_events(
    *,
    limit: int = 20,
    db_path: str | Path | None = None,
) -> list[dict[str, str | float | int]]:
    path = initialize_database(db_path)
    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, question, predicted_category, confidence, created_at
            FROM question_events
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()

    return [
        {
            "id": int(row["id"]),
            "question": str(row["question"]),
            "predicted_category": str(row["predicted_category"]),
            "confidence": float(row["confidence"]),
            "created_at": str(row["created_at"]),
        }
        for row in rows
    ]