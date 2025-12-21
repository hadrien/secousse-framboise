#!/bin/bash
set -e

echo "Uninstalling Radio Secousse..."

# Stop and disable services
systemctl stop secousse secousse-web || true
systemctl disable secousse secousse-web || true

# Remove service files
rm -f /etc/systemd/system/secousse.service
rm -f /etc/systemd/system/secousse-web.service

# Remove application directory
rm -rf /opt/secousse-web

# Remove config directory
rm -rf /etc/secousse

# Reload systemd
systemctl daemon-reload

echo "Radio Secousse uninstalled!"
