FROM rust:latest AS librespot-builder
RUN apt-get update && apt-get install -y libasound2 libasound2-dev pkg-config
RUN cargo install --locked librespot

FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/TonieAudioHub/client/package*.json ./
RUN npm install
COPY frontend/TonieAudioHub/client/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    nginx \
    supervisor \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy application files
COPY worker/ ./worker/
COPY connect/ ./connect/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create required directories
RUN mkdir -p /fifo /app/output /app/db

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy librespot binary from build stage
COPY --from=librespot-builder /usr/local/cargo/bin/librespot /usr/local/bin/librespot

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
