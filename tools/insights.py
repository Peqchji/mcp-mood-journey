from collections import Counter
import re
from storage.db import load_entries
from utils.builders import ResponseBuilder
from datetime import datetime, timedelta

stop_words = {'the', 'and', 'was', 'for', 'with', 'that', 'this', 'but', 'not', 'have', 'from', 'had'}

def list_emotions():
    """Show all unique emotion tags you've used."""
    entries = load_entries()
    uniqueEntry = set()
    for entry in entries:
        uniqueEntry.add(entry["emotion"])

    return ResponseBuilder.success(
        f"Found {len(uniqueEntry)} unique emotions", 
        uniqueEntry
    )

def get_streak():
    """Check your current logging streak."""
    entries = load_entries()
    if not entries:
        return ResponseBuilder.success("No entries yet", {"streak": 0})

    timestamp = set()
    for entry in entries:
        timestamp.add(entry["timestamp"][:10])

    # unique dates with entries, sorted descending
    dates = sorted(
        list(timestamp),
        reverse=True
    )
    
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    if len(dates) == 0 or dates[0] not in [today, yesterday]:
        return ResponseBuilder.success("No current streak", {"streak": 0})
    
    streak = 1
    current_date = datetime.strptime(dates[0], "%Y-%m-%d")
    
    for i in range(1, len(dates)):
        prev_date = datetime.strptime(dates[i], "%Y-%m-%d")
        if (current_date - prev_date).days == 1:
            streak += 1
            current_date = prev_date
        else:
            break
            
    return ResponseBuilder.success(f"Current streak: {streak} days", {"streak": streak})

def find_patterns():
    """
    Detect recurring moods and keyword correlations.
    Prioritizes keyword correlation in notes.
    """
    entries = load_entries()
    if not entries:
        return ResponseBuilder.success("Not enough data to find patterns", {})

    keywords = Counter()
    emotion_keywords = {} # emotion -> list of words
    
    for e in entries:
        note = e.get("note") or ""
        emotion = e["emotion"].lower()
        if note:
            words = re.findall(r'\w+', note.lower())
            words = [w for w in words if len(w) > 2 and w not in stop_words]
            
            if emotion not in emotion_keywords:
                emotion_keywords[emotion] = Counter()

            emotion_keywords[emotion].update(words)
            keywords.update(words)

    # Correlate emotions with keywords
    correlations = {}
    for emotion, counts in emotion_keywords.items():
        top_words = [word for word, count in counts.most_common(3)]
        if top_words:
            correlations[emotion] = top_words

    day_scores = {}
    day_counts = {}
    for e in entries:
        day = e["day_of_week"]
        day_scores[day] = day_scores.get(day, 0) + e["score"]
        day_counts[day] = day_counts.get(day, 0) + 1
    
    day_averages = {day: round(day_scores[day] / day_counts[day], 2) for day in day_scores}

    patterns = {
        "keyword_correlations": correlations,
        "day_of_week_averages": day_averages,
        "total_entries": len(entries)
    }
    
    return ResponseBuilder.success("Pattern analysis complete", patterns)
