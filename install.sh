#!/bin/bash
set -e

echo "Installing Radio Secousse..."

# Install ffmpeg (includes ffplay)
apt-get update
apt-get install -y ffmpeg

# Download and install the systemd service file
curl -fsSL -H "Cache-Control: no-cache" https://raw.githubusercontent.com/hadrien/secousse-framboise/main/secousse.service -o /etc/systemd/system/secousse.service

# Reload systemd and enable the service
systemctl daemon-reload
systemctl enable secousse
systemctl restart secousse

echo "Radio Secousse installed and started!"
echo "Check status with: systemctl status secousse"
