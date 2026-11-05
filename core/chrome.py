
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE = str(BASE_DIR / "chrome-profile")
PORT = 9222


def find_chrome():
    candidates = [
        os.environ.get("CHROME_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ),
        shutil.which("chrome"),
        shutil.which("google-chrome"),
    ]

    for path in candidates:
        if path and Path(path).is_file():
            return path

    sys.exit(
        "Google Chrome tidak ditemukan. "
        "Atur environment variable CHROME_PATH."
    )


def start_chrome(urls=(), debug=False):
    args = [
        find_chrome(),
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
    ]

    if debug:
        args.append(f"--remote-debugging-port={PORT}")

    subprocess.Popen(args + list(urls))


def wait_port(seconds=30):
    for _ in range(seconds):
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{PORT}/json/version",
                timeout=1,
            ):
                return True
        except Exception:
            time.sleep(1)

    return False
