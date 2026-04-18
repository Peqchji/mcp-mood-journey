from storage.db import add_entry
from utils.builders import ResponseBuilder, Errors

def log_mood(mood: str, score: int, note: str = None):
    """Log current mood with score and optional note."""
    try:
        if not (1 <= score <= 10):
            return Errors.INVALID_SCORE
        
        entry = add_entry(score=score, emotion=mood, note=note)
        
        return ResponseBuilder.success(f"Logged {mood} (score: {score})", entry)
    except Exception as e:
        return Errors.INTERNAL_ERROR
