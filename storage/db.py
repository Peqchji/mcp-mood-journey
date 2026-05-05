import json
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
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
        return None

def delete_entry_by_id(entry_id: str):
    entries = load_entries()
    original_count = len(entries)
    entries = [e for e in entries if e["id"] != entry_id]

    if len(entries) < original_count:
        save_entries(entries)

        return True

    return False

def get_entries_by_date(date_str: str):
    """date_str in YYYY-MM-DD format"""
    entries = load_entries()

    return [e for e in entries if e["timestamp"].startswith(date_str)]

def get_entries_by_range(start_date: str = None, end_date: str = None):
    """dates in YYYY-MM-DD format"""
    entries = load_entries()
    filtered = entries
    if start_date:
        filtered = [e for e in filtered if e["timestamp"] >= start_date]
    
    if end_date:
        # Append T23:59:59 to end_date to include the whole day
        end_date_full = f"{end_date}T23:59:59"
        filtered = [e for e in filtered if e["timestamp"] <= end_date_full]
    
    return filtered

def search_entries_by_text(query: str):
    entries = load_entries()
    query = query.lower()
    
    return [
        e for e in entries 
        if query in (e.get("note") or "").lower() or query in e["emotion"].lower()
    ]

