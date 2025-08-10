# Tonies Audio Prepper

A Dockerized system for capturing Spotify audio via Spotify Connect, automatically processing it for Kreativ-Tonies, and providing a web dashboard for status, sessions, tracks, logs, and monitoring.

## Features

- **Spotify Connect** audio capture (no desktop loopback)
- **Automatic audio processing** (LUFS normalization, tagging, splitting, packaging)
- **Web dashboard** (FastAPI, German UI)
- **Session & track management** (SQLite)
- **Live logs & monitoring**
- **Multi-platform**: Runs on Linux, macOS, Windows, Raspberry Pi

## Repository Structure

- `connect/` – Spotify Connect receiver (librespot, PCM to FIFO)
- `worker/` – Audio pipeline, FastAPI backend, database, web UI
- `frontend/TonieAudioHub/client/` – React/TypeScript frontend (served by backend)
- `output/` – Processed MP3 files and session folders
- `db/` – SQLite database
- `fifo/` – Named pipe for PCM audio exchange
- `Dockerfile` – Unified build for frontend and backend
- `docker-compose.yml` – Compose file for running the app
- `AGENT.md` – Full technical specification and code details

## How to Build & Run

### Build and Push Multi-Arch Image

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/sheldoreb/tonie_converter-app:latest --push .
```

### Run Locally (Single Container)

```bash
docker compose up -d
```

- The web dashboard is available at: [http://localhost:8080](http://localhost:8080)
- API endpoints are under `/api/` (see AGENT.md for details)

### Volumes

- `spotpipe` – Named volume for FIFO exchange
- `./output` – Output MP3 files and session folders
- `./db` – SQLite database

## Sources & Documentation

- **Backend & API:** `worker/`
- **Frontend:** `frontend/TonieAudioHub/client/`
- **Connect/Audio:** `connect/`
- **Specs & Code Details:** See [`AGENT.md`](./AGENT.md) for architecture, API, pipeline, and UI details.
