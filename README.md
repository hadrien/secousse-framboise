# secousse-framboise

Play Radio Secousse on your Raspberry Pi as a systemd service.

## Prerequisites

- Raspberry Pi with Debian-based OS (Raspberry Pi OS, Raspbian, etc.)
- Audio output configured (HDMI, 3.5mm jack, or USB audio)
- Internet connection

## Install

```bash
curl -fsSL -H "Cache-Control: no-cache" https://raw.githubusercontent.com/hadrien/secousse-framboise/main/install.sh | sudo bash
```

## Uninstall

```bash
curl -fsSL -H "Cache-Control: no-cache" https://raw.githubusercontent.com/hadrien/secousse-framboise/main/uninstall.sh | sudo bash
```

## Usage

Check service status:

```bash
systemctl status secousse
```

View logs:

```bash
journalctl -u secousse -f
```
