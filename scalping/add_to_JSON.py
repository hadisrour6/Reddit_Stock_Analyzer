# file: tracker.py
import json
from pathlib import Path

FILENAME = Path("tracker.json")

def add_snapshot(entry: dict):
    # Load or initialize the JSON dict
    data = {}
    if FILENAME.exists():
        with FILENAME.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    sub = entry["subreddit_Name"]

    # Ensure subreddit dict and its history list exist (without resetting)
    data.setdefault(sub, {}).setdefault("history", [])

    # Append the new snapshot (keeps all existing data intact)
    data[sub]["history"].append(entry)

    # Save back
    with FILENAME.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)