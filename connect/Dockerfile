FROM rust:latest
RUN apt-get update && apt-get install -y libasound2 libasound2-dev pkg-config
RUN cargo install librespot
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
