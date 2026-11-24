import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "hiresense.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS screenings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate TEXT,
                score REAL,
                required_score REAL,
                preferred_score REAL,
                matched_skills TEXT,
                missing_skills TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_screening(df):
    if df.empty:
        return

    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        for _, row in df.iterrows():
            conn.execute("""
                INSERT INTO screenings
                (candidate, score, required_score, preferred_score,
                 matched_skills, missing_skills, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row.get("Candidate", "")),
                float(row.get("Score (%)", 0)),
                float(row.get("Required Score (%)", 0)),
                float(row.get("Preferred Score (%)", 0)),
                str(row.get("Matched Skills", "")),
                str(row.get("Missing Skills", "")),
                str(row.get("Status", ""))
            ))


def get_screening_history():
    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM screenings ORDER BY created_at DESC",
            conn
        )


def clear_screening_history():
    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM screenings")