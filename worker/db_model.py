import sqlite3
from typing import Optional

DB_PATH = '/app/db/tonie.db'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    started_at TEXT,
    ended_at TEXT,
    name TEXT,
    artist TEXT,
    preset TEXT,
    total_duration_s INTEGER,
    lufs_avg REAL,
    tonie_index INTEGER
);
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    idx INTEGER,
    title TEXT,
    artist TEXT,
    album TEXT,
    duration_s INTEGER,
    lufs REAL,
    true_peak REAL,
    path TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    ts TEXT,
    level TEXT,
    msg TEXT,
    session_id INTEGER,
    track_id INTEGER
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS auth_tokens (
    id INTEGER PRIMARY KEY,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TEXT
);
'''

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

init_db()
