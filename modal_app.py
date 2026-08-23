from __future__ import annotations

import subprocess
from pathlib import Path

import modal

ROOT = Path(__file__).parent
PORT = 8000

image = modal.Image.debian_slim(python_version="3.12").add_local_dir(
    ROOT,
    remote_path="/app",
    copy=True,
    ignore=[".git", ".venv", ".pytest_cache", ".ruff_cache", "__pycache__"],
)
app = modal.App("northstar-demo-production")


@app.function(
    image=image,
    cpu=0.125,
    memory=128,
    min_containers=0,
    max_containers=1,
    scaledown_window=60,
)
@modal.concurrent(max_inputs=50)
@modal.web_server(PORT, startup_timeout=20)
def storefront() -> None:
    subprocess.Popen(["python", "/app/app.py"], cwd="/app")
