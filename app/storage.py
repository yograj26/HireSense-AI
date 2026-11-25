import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "hiresense.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_screening(candidate_name, score, matched_skills, missing_skills):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO screenings
        (candidate_name, score, matched_skills, missing_skills)
        VALUES (?, ?, ?, ?)
    """, (
        candidate_name,
        score,
        ", ".join(matched_skills),
        ", ".join(missing_skills)
    ))
    conn.commit()
    conn.close()

def get_screening_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM screenings ORDER BY created_at DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM screenings")
    conn.commit()
    conn.close()