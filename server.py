import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, EmbeddedResource
from tools.log import log_mood
from enum import Enum


app = Server("mood-journey")

class ToolName(str, Enum):
    LOG_MOOD = "log_mood"

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
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == ToolName.LOG_MOOD:
        return log_mood(**arguments)
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
