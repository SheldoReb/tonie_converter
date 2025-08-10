FROM rust:latest
RUN apt-get update && apt-get install -y libasound2
RUN cargo install librespot
CMD ["librespot", "--name", "${NAME}", "--backend", "${BACKEND}", "--device", "${DEVICE}", "--bitrate", "${BITRATE}", "--volume-normalisation", "${VOLUME_NORMALISATION}"]
