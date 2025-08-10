from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from db_model import DB_PATH

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

@app.get("/")
async def root():
    return RedirectResponse(url="/api/status")

@app.get("/api/status")
def get_status(db=Depends(get_db)):
    # Dummy status
    return {
        "state": "idle",
        "current": None,
        "preset": "speech",
        "output_dir": "/app/output",
        "active_session_id": None
    }

@app.get("/api/sessions")
def get_sessions(db=Depends(get_db)):
    cur = db.execute('SELECT * FROM sessions ORDER BY started_at DESC')
    return [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]

@app.get("/api/sessions/{id}")
def get_session(id: int, db=Depends(get_db)):
    cur = db.execute('SELECT * FROM sessions WHERE id = ?', (id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(404, 'Session not found')
    return dict(zip([column[0] for column in cur.description], row))

@app.get("/api/tracks")
def get_tracks(session_id: int, db=Depends(get_db)):
    cur = db.execute('SELECT * FROM tracks WHERE session_id = ? ORDER BY idx', (session_id,))
    return [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]

@app.get("/api/logs/stream")
def stream_logs():
    def event_stream():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.execute('SELECT ts, level, msg FROM events ORDER BY ts DESC LIMIT 100')
        for row in cur.fetchall():
            yield f"data: {row}\n\n"
        conn.close()
    return StreamingResponse(event_stream(), media_type="text/event-stream")
