import sqlite3
from db_model import DB_PATH

def add_track(session_id, idx, title, artist, album, duration_s, lufs, true_peak, path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''INSERT INTO tracks (session_id, idx, title, artist, album, duration_s, lufs, true_peak, path, created_at)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime())''',
                (session_id, idx, title, artist, album, duration_s, lufs, true_peak, path))
    track_id = cur.lastrowid
    conn.commit()
    conn.close()
    return track_id
