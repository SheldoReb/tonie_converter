import sqlite3
from db_model import DB_PATH

def start_session(name, artist, preset, tonie_index=1):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO sessions (started_at, name, artist, preset, tonie_index) VALUES (datetime(), ?, ?, ?, ?)',
                (name, artist, preset, tonie_index))
    session_id = cur.lastrowid
    conn.commit()
    conn.close()
    return session_id

def end_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('UPDATE sessions SET ended_at = datetime() WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()
