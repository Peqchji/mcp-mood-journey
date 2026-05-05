from datetime import datetime, timedelta
from storage.db import get_entries_by_date, get_entries_by_range, search_entries_by_text
from utils.builders import ResponseBuilder

def get_today():
    """Retrieve today's mood entries."""
    today = datetime.now().strftime("%Y-%m-%d")
    entries = get_entries_by_date(today)

    return ResponseBuilder.success(f"Found {len(entries)} entries for today", entries)

def get_mood_summary(start_date: str = None, end_date: str = None, period: str = None):
    """
    Weekly/monthly mood summary with averages.
    period can be 'weekly' or 'monthly'.
    """
    if period:
        end = datetime.now()
        if period == "weekly":
            start = end - timedelta(days=7)
        elif period == "monthly":
            start = end - timedelta(days=30)
        else:
            return ResponseBuilder.error(f"Invalid period: {period}. Use 'weekly' or 'monthly'.")
        
        start_date = start.strftime("%Y-%m-%d")
        end_date = end.strftime("%Y-%m-%d")

    entries = get_entries_by_range(start_date, end_date)
    
    if not entries:
        return ResponseBuilder.success("No entries found for this period", {"avg_score": 0, "count": 0})

    avg_score = sum(e["score"] for e in entries) / len(entries)
    
    summary = {
        "period": f"{start_date} to {end_date}" if start_date and end_date else "All time",
        "avg_score": round(avg_score, 2),
        "count": len(entries),
        "entries": entries
    }
    
    return ResponseBuilder.success("Mood summary calculated", summary)

def search_entries(query: str):
    """Search past entries by keyword or emotion."""
    entries = search_entries_by_text(query)
    
    return ResponseBuilder.success(f"Found {len(entries)} entries matching '{query}'", entries)
