import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, EmbeddedResource
from tools.log import log_mood, delete_entry
from tools.query import get_today, get_mood_summary, search_entries
from tools.insights import find_patterns, get_streak, list_emotions
from tools.export import export_data
from enum import Enum


app = Server("mood-journey")

class ToolName(str, Enum):
    LOG_MOOD = "log_mood"
    DELETE_ENTRY = "delete_entry"
    GET_TODAY = "get_today"
    GET_MOOD_SUMMARY = "get_mood_summary"
    SEARCH_ENTRIES = "search_entries"
    FIND_PATTERNS = "find_patterns"
    GET_STREAK = "get_streak"
    LIST_EMOTIONS = "list_emotions"
    EXPORT_DATA = "export_data"

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name=ToolName.LOG_MOOD,
            description="Log current mood with score (1-10) and optional note",
            inputSchema={
                "type": "object",
                "properties": {
                    "mood": {"type": "string", "description": "Emotion label (e.g., anxious, calm)"},
                    "score": {"type": "integer", "description": "Mood score from 1-10"},
                    "note": {"type": "string", "description": "Optional context or notes"}
                },
                "required": ["mood", "score"]
            }
        ),
        Tool(
            name=ToolName.DELETE_ENTRY,
            description="Delete a mood entry by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "entry_id": {"type": "string", "description": "ID of the entry to delete (e.g., 20250228-001)"}
                },
                "required": ["entry_id"]
            }
        ),
        Tool(
            name=ToolName.GET_TODAY,
            description="Retrieve today's mood entries",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name=ToolName.GET_MOOD_SUMMARY,
            description="Weekly/monthly mood summary with averages",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {"type": "string", "description": "Predefined period: 'weekly' or 'monthly'"},
                    "start_date": {"type": "string", "description": "Custom start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "Custom end date (YYYY-MM-DD)"}
                }
            }
        ),
        Tool(
            name=ToolName.SEARCH_ENTRIES,
            description="Search past entries by keyword or emotion",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Keyword or emotion to search for"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name=ToolName.FIND_PATTERNS,
            description="Detect recurring moods and keyword correlations in notes",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name=ToolName.GET_STREAK,
            description="Check your current logging streak",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name=ToolName.LIST_EMOTIONS,
            description="Show all unique emotion tags you've used",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name=ToolName.EXPORT_DATA,
            description="Export all mood data (optimized for AI agent consumption)",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {"type": "string", "enum": ["csv", "json"], "description": "Export format (default: csv)"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == ToolName.LOG_MOOD:
        return log_mood(**arguments)
    elif name == ToolName.DELETE_ENTRY:
        return delete_entry(**arguments)
    elif name == ToolName.GET_TODAY:
        return get_today()
    elif name == ToolName.GET_MOOD_SUMMARY:
        return get_mood_summary(**arguments)
    elif name == ToolName.SEARCH_ENTRIES:
        return search_entries(**arguments)
    elif name == ToolName.FIND_PATTERNS:
        return find_patterns()
    elif name == ToolName.GET_STREAK:
        return get_streak()
    elif name == ToolName.LIST_EMOTIONS:
        return list_emotions()
    elif name == ToolName.EXPORT_DATA:
        return export_data(**arguments)
    raise ValueError(f"Tool not found: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
