
import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_listing(listing):
    listing_path = Path(listing)

    if not listing_path.is_absolute():
        listing_path = BASE_DIR / listing_path

    if not listing_path.is_file():
        sys.exit(f"File listing tidak ditemukan: {listing_path}")

    try:
        return json.loads(
            listing_path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as e:
        sys.exit(f"Format JSON tidak valid: {e}")
