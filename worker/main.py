from fastapi import FastAPI
app = FastAPI()

@app.get("/api/status")
def get_status():
    return {
        "state": "idle",
        "current": None,
        "preset": "speech",
        "output_dir": "/app/output",
        "active_session_id": None
    }
