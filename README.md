# secousse-framboise

Play Radio Secousse on your Raspberry Pi with a retro jukebox web interface.

> [!IMPORTANT]
> **Support Radio Secousse!** [Subscribe $ at secousse.tv](https://secousse.tv)


## Features

- Stream 8 Radio Secousse channels: RADIO, PARTY, CHILL, STREET, TRIPPY, JAH BLESS, HILLBILLY, OLÉ
- Retro jukebox-style web UI accessible from any device on your network
- Runs as systemd services for automatic startup
- Stream selection persists across reboots

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

### Web Interface

Open your browser and navigate to your Raspberry Pi's IP address:

```
http://<raspberry-pi-ip>/
```

Click any stream button to switch channels. The active stream is highlighted.

### Command Line

Check service status:

```bash
systemctl status secousse      # Audio player service
systemctl status secousse-web  # Web interface service
```

View logs:

```bash
journalctl -u secousse -f      # Audio player logs
journalctl -u secousse-web -f  # Web interface logs
```

### Configuration

The current stream is stored in `/etc/secousse/stream.conf` and persists across reinstalls.

Audio device is configured in `/etc/systemd/system/secousse.service` via the `AUDIODEV` environment variable (default: `plughw:1,0`).

## Architecture

- **secousse.service** - Runs `ffplay` to stream audio
- **secousse-web.service** - FastAPI app (uvicorn) serving the web UI on port 80
- **uv** - Python package manager (installed automatically)

## Development

```bash
# Install dependencies
uv sync

# Run the web app locally
uv run uvicorn app.main:app --reload
```
