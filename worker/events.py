import time
import sqlite3
from db_model import DB_PATH

def log_event(level, msg, session_id=None, track_id=None):
    conn = sqlite3.connect(DB_PATH)
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO events (ts, level, msg, session_id, track_id) VALUES (?, ?, ?, ?, ?)',
                 (ts, level, msg, session_id, track_id))
    conn.commit()
    conn.close()
