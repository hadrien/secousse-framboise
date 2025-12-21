import subprocess
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

STREAMS = {
    "secousse": "RADIO",
    "secousse-party": "PARTY",
    "secousse-chill": "CHILL",
    "secousse-street": "STREET",
    "secousse-trippy": "TRIPPY",
    "secousse-jahbless": "JAH BLESS",
    "secousse-hillbilly": "HILLBILLY",
    "secousse-ole": "OLE!",
}

CONFIG_PATH = Path("/etc/secousse/stream.conf")


def get_current_stream() -> str:
    try:
        return CONFIG_PATH.read_text().strip()
    except FileNotFoundError:
        return "secousse"


def set_current_stream(stream: str) -> None:
    CONFIG_PATH.write_text(stream)
    subprocess.run(["systemctl", "restart", "secousse"], check=True)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Radios</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background-color: #7B5CD6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            font-family: Arial, sans-serif;
        }}
        h1 {{
            color: #000;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .divider {{
            width: 100%;
            max-width: 600px;
            height: 8px;
            background-color: #fff;
            margin-bottom: 20px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            width: 100%;
            max-width: 600px;
        }}
        .btn {{
            background: linear-gradient(to bottom, #F5E6C8 0%, #E8D4A8 60%, #C9A86C 100%);
            border: 4px solid #2D2D2D;
            border-radius: 8px;
            padding: 25px 15px;
            font-size: 1.8rem;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            box-shadow: 
                0 6px 0 #8B7355,
                0 8px 10px rgba(0,0,0,0.3);
            transition: all 0.1s ease;
            text-transform: uppercase;
        }}
        .btn:hover {{
            transform: translateY(2px);
            box-shadow: 
                0 4px 0 #8B7355,
                0 6px 8px rgba(0,0,0,0.3);
        }}
        .btn:active {{
            transform: translateY(4px);
            box-shadow: 
                0 2px 0 #8B7355,
                0 4px 6px rgba(0,0,0,0.3);
        }}
        .btn.active {{
            background: linear-gradient(to bottom, #E85D4C 0%, #D64A3A 60%, #B33A2C 100%);
            color: #000;
        }}
        .btn-radio {{ font-family: Impact, sans-serif; }}
        .btn-party {{ font-family: "Arial Black", sans-serif; font-weight: 900; }}
        .btn-chill {{ font-family: "Trebuchet MS", sans-serif; letter-spacing: 3px; }}
        .btn-street {{ font-family: "Times New Roman", serif; font-style: italic; }}
        .btn-trippy {{ font-family: Impact, sans-serif; letter-spacing: 2px; }}
        .btn-jahbless {{ font-family: "Arial Black", sans-serif; }}
        .btn-hillbilly {{ font-family: "Courier New", monospace; font-weight: bold; }}
        .btn-ole {{ font-family: "Georgia", serif; font-style: italic; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>The Radios</h1>
    <div class="divider"></div>
    <div class="grid">
        {buttons}
    </div>
    <script>
        async function selectStream(stream) {{
            const buttons = document.querySelectorAll('.btn');
            buttons.forEach(btn => btn.disabled = true);
            
            try {{
                const response = await fetch(`/stream/${{stream}}`, {{ method: 'POST' }});
                if (response.ok) {{
                    buttons.forEach(btn => btn.classList.remove('active'));
                    document.querySelector(`[data-stream="${{stream}}"]`).classList.add('active');
                }}
            }} catch (error) {{
                console.error('Failed to change stream:', error);
            }} finally {{
                buttons.forEach(btn => btn.disabled = false);
            }}
        }}
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    current = get_current_stream()
    buttons = []
    btn_classes = {
        "secousse": "btn-radio",
        "secousse-party": "btn-party",
        "secousse-chill": "btn-chill",
        "secousse-street": "btn-street",
        "secousse-trippy": "btn-trippy",
        "secousse-jahbless": "btn-jahbless",
        "secousse-hillbilly": "btn-hillbilly",
        "secousse-ole": "btn-ole",
    }
    for stream_id, label in STREAMS.items():
        active = "active" if stream_id == current else ""
        btn_class = btn_classes.get(stream_id, "")
        buttons.append(
            f'<button class="btn {btn_class} {active}" data-stream="{stream_id}" '
            f"onclick=\"selectStream('{stream_id}')\">{label}</button>"
        )
    return HTML_TEMPLATE.format(buttons="\n        ".join(buttons))


@app.post("/stream/{stream_id}")
async def change_stream(stream_id: str):
    if stream_id not in STREAMS:
        return {"error": "Invalid stream"}, 400
    set_current_stream(stream_id)
    return {"status": "ok", "stream": stream_id}


@app.get("/api/status")
async def status():
    return {"stream": get_current_stream()}
