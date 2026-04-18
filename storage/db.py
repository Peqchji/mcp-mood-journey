import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DB_FILE = DATA_DIR / "moods.json"

def init_db():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
    if not DB_FILE.exists():
        with open(DB_FILE, "w") as f:
            json.dump({"entries": []}, f)

def load_entries():
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)["entries"]

def save_entries(entries):
    with open(DB_FILE, "w") as f:
        json.dump({"entries": entries}, f, indent=2)

class EntryBuilder:
    def __init__(self, score, emotion, note=None):
        self.score = score
        self.emotion = emotion
        self.note = note
        self.timestamp = datetime.now()

    def build(self, current_entries_count):
        return {
            "id": f"{self.timestamp.strftime('%Y%m%d')}-{current_entries_count + 1:03d}",
            "timestamp": self.timestamp.isoformat(),
            "score": self.score,
            "emotion": self.emotion,
            "note": self.note,
            "day_of_week": self.timestamp.strftime("%A")
        }

def add_entry(score, emotion, note=None):
    try:
        entries = load_entries()
        builder = EntryBuilder(score, emotion, note)
        new_entry = builder.build(len(entries))
        entries.append(new_entry)
        
        save_entries(entries)

        return new_entry
    except Exception as e:
        return Errors.INTERNAL_ERROR

    return new_entry
