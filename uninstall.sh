#!/bin/bash
set -e

echo "Uninstalling Radio Secousse..."

# Stop and disable the service
systemctl stop secousse || true
systemctl disable secousse || true

# Remove the service file
rm -f /etc/systemd/system/secousse.service

# Reload systemd
systemctl daemon-reload

echo "Radio Secousse uninstalled!"
