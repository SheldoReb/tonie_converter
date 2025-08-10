#!/bin/bash

exec librespot \
  --name "$NAME" \
  --backend "$BACKEND" \
  --device "$DEVICE" \
  --bitrate "$BITRATE" \
  --volume-ctrl "${VOLUME_CTRL:-fixed}" \
  --initial-volume "${INITIAL_VOLUME:-100}"
