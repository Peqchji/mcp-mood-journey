from storage.db import add_entry, delete_entry_by_id
from utils.builders import ResponseBuilder, Errors

def log_mood(mood: str, score: int, note: str = None):
    """Log current mood with score and optional note."""
    try:
        if not (1 <= score <= 10):
            return Errors.INVALID_SCORE
        
        entry = add_entry(score=score, emotion=mood, note=note)
        if not entry:
            return Errors.INTERNAL_ERROR
        
        return ResponseBuilder.success(f"Logged {mood} (score: {score})", entry)
    except Exception as e:
        return Errors.INTERNAL_ERROR

def delete_entry(entry_id: str):
    """Delete a mood entry by ID."""
    if delete_entry_by_id(entry_id):
        return ResponseBuilder.success(f"Deleted entry {entry_id}")

    return Errors.NOT_FOUND

