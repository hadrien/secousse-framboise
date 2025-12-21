#!/bin/bash
set -e

echo "Installing Radio Secousse..."

# Install system dependencies
apt-get update
apt-get install -y ffmpeg curl unzip

# Install uv
if ! command -v /root/.local/bin/uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Download repo as zip and extract to /opt/secousse-web
echo "Downloading secousse-framboise..."
curl -fsSL -H "Cache-Control: no-cache" -L https://github.com/hadrien/secousse-framboise/archive/refs/heads/main.zip -o /tmp/secousse.zip
rm -rf /opt/secousse-web
unzip -q /tmp/secousse.zip -d /opt
mv /opt/secousse-framboise-main /opt/secousse-web
rm /tmp/secousse.zip

# Install Python dependencies
echo "Installing Python dependencies..."
cd /opt/secousse-web && /root/.local/bin/uv sync

# Create config directory and default config (preserve existing selection)
mkdir -p /etc/secousse
[ -f /etc/secousse/stream.conf ] || echo "secousse" > /etc/secousse/stream.conf

# Install service files
cp /opt/secousse-web/secousse.service /etc/systemd/system/
cp /opt/secousse-web/secousse-web.service /etc/systemd/system/

# Reload systemd and enable services
systemctl daemon-reload
systemctl enable secousse secousse-web
systemctl restart secousse secousse-web

echo ""
echo "Radio Secousse installed and started!"
echo "Web UI available at: http://$(hostname -I | awk '{print $1}')"
echo "Check status with: systemctl status secousse secousse-web"
