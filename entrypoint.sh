#!/bin/bash
set -e

# Start nginx
nginx

# Start the backend API (runs on port 8000 internally)
cd /app/worker
gunicorn main:app --bind 127.0.0.1:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker &

# Start the connect service
cd /app/connect
python3 connect.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
