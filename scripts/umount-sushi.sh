#!/bin/bash
# Unmount sushi's directory

MOUNT_POINT="$HOME/sushi-videos"

if mount | grep -q "$MOUNT_POINT"; then
  echo "Unmounting $MOUNT_POINT..."
  umount "$MOUNT_POINT"
  echo "✓ Unmounted"
else
  echo "Not mounted"
fi
