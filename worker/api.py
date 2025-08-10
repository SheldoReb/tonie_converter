from fastapi import FastAPI, Depends, HTTPException, Request, Query
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import json
from typing import Optional
from pydantic import BaseModel
from db_model import DB_PATH

# Pydantic models for request/response validation
class ConfigUpdate(BaseModel):
    preset: Optional[str] = None
    target_lufs: Optional[float] = None
    true_peak: Optional[float] = None
    bitrate_k: Optional[int] = None
    mono: Optional[bool] = None
    max_tonie_min: Optional[int] = None

app = FastAPI(
    title="Tonie Converter API",
    description="API for managing audio conversion sessions and tracks for Tonie boxes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOW_ORIGINS", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    cur = db.execute('SELECT value FROM settings WHERE key = ?', ('preset',))
    preset = cur.fetchone()
    preset = preset[0] if preset else 'speech'

    return {
        "state": "idle",  # TODO: Implement state tracking
        "current": None,
        "preset": preset,
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
def get_tracks(
    session_id: int = Query(..., description="ID of the session to get tracks for"),
    db=Depends(get_db)
):
    cur = db.execute('SELECT * FROM tracks WHERE session_id = ? ORDER BY idx', (session_id,))
    return [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]

@app.get("/api/config")
def get_config(db=Depends(get_db)):
    cur = db.execute('SELECT key, value FROM settings')
    settings = dict(cur.fetchall())
    
    return {
        "preset": settings.get('preset', 'speech'),
        "target_lufs": float(settings.get('target_lufs', -18.0)),
        "true_peak": float(settings.get('true_peak', -1.0)),
        "bitrate_k": int(settings.get('bitrate_k', 96)),
        "mono": settings.get('mono', '1') == '1',
        "max_tonie_min": int(settings.get('max_tonie_min', 90)),
        "spotify_integration": bool(settings.get('spotify_client_id')),
        "prometheus_metrics": settings.get('enable_metrics', '0') == '1'
    }

@app.put("/api/config")
def update_config(config: ConfigUpdate, db=Depends(get_db)):
    updates = config.model_dump(exclude_unset=True)
    
    for key, value in updates.items():
        db.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                  (key, str(value)))
    
    db.commit()
    return get_config(db)

@app.get("/api/logs/stream")
def stream_logs():
    def event_stream():
        conn = sqlite3.connect(DB_PATH)
        try:
            while True:
                cur = conn.execute('''
                    SELECT ts, level, msg, session_id, track_id 
                    FROM events 
                    ORDER BY ts DESC 
                    LIMIT 100
                ''')
                for row in cur.fetchall():
                    yield f"data: {json.dumps(dict(zip(['ts', 'level', 'msg', 'session_id', 'track_id'], row)))}\n\n"
        finally:
            conn.close()
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/api/spotify/auth")
async def spotify_auth():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    if not client_id or not redirect_uri:
        raise HTTPException(400, "Spotify integration not configured")
    
    auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    return {"url": auth_url}

@app.get("/api/spotify/callback")
async def spotify_callback(code: str, db=Depends(get_db)):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    if not all([client_id, client_secret, redirect_uri]):
        raise HTTPException(400, "Spotify integration not configured")
    
    # TODO: Implement token exchange
    return {"status": "success"}

@app.get("/metrics")
async def metrics():
    if os.getenv("ENABLE_METRICS", "0") != "1":
        raise HTTPException(404, "Metrics not enabled")
        
    # TODO: Implement Prometheus metrics collection
    metrics_output = """
    # HELP tonie_sessions_total Total number of conversion sessions
    # TYPE tonie_sessions_total counter
    tonie_sessions_total{state="completed"} 0
    """
    return PlainTextResponse(metrics_output.strip())
