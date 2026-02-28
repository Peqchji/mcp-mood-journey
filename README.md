# 🌱 Mood Journey — MCP Server

> A personal mood tracking MCP server that lets Claude log your emotions, spot patterns, and reflect on your mental wellness journey — all stored **locally on your machine**. No cloud. No subscriptions. Just you.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![MCP](https://img.shields.io/badge/MCP-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Storage](https://img.shields.io/badge/Storage-Local%20JSON-orange)
![uv](https://img.shields.io/badge/package%20manager-uv-purple)

---

## 📌 What Is This?

**Mood Journey** is a local MCP server that turns Claude into your personal mood companion. Log how you feel through natural conversation, then ask Claude to find patterns, celebrate wins, or reflect on tough weeks — all without your data ever leaving your computer.

**Example conversations after setup:**
```
You:    "I'm feeling really anxious about my job interview tomorrow."
Claude: → calls log_mood(mood="anxious", note="job interview tomorrow", score=3)
Claude: "Logged. You've actually felt this way before big events — last time
         you bounced back quickly. You've got this. 💪"
```

```
You:    "How have I been feeling this month?"
Claude: → calls get_mood_summary(period="this_month")
Claude: "This month your average mood score was 6.8/10 — your best month
         in 3 months! You had 14 good days and 4 tough ones. Mondays
         tend to be your hardest day..."
```

---

## ✨ Features

| Tool | Description |
|------|-------------|
| `log_mood` | Log current mood with score, emotion tag, and optional note |
| `get_today` | Retrieve today's mood entries |
| `get_mood_summary` | Weekly/monthly mood summary with averages |
| `find_patterns` | Detect recurring moods by day, time, or trigger keyword |
| `get_streak` | Check your current logging streak |
| `list_emotions` | Show all emotion tags you've used |
| `search_entries` | Search past entries by keyword or emotion |
| `delete_entry` | Remove a specific entry by ID |
| `export_data` | Export all data to CSV for personal use |

---

## 🔒 Privacy First

| Feature | Detail |
|---------|--------|
| **Storage** | 100% local — plain `.json` file on your machine |
| **No cloud** | Zero data sent to any server |
| **No auth** | No accounts, no API keys |
| **Portable** | Your data file is just JSON — readable by any tool |
| **Deletable** | One command wipes everything |

> 💡 Your mood data is sensitive. This project is intentionally designed to **never leave your device**.

---

## 🗂️ Project Structure

```
mood-journey-mcp/
├── server.py                  # MCP server entry point
├── tools/
│   ├── __init__.py
│   ├── log.py                 # log_mood, delete_entry
│   ├── query.py               # get_today, get_mood_summary, search_entries
│   ├── insights.py            # find_patterns, get_streak, list_emotions
│   └── export.py              # export_data to CSV
├── storage/
│   ├── __init__.py
│   └── db.py                  # Read/write local JSON file
├── data/
│   └── moods.json             # Your mood data (auto-created, gitignored)
├── tests/
│   ├── test_log.py
│   └── test_query.py
├── pyproject.toml             # Project metadata + dependencies (managed by uv)
├── uv.lock                    # Lockfile (commit this!)
├── .gitignore                 # moods.json is always ignored
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- [Claude Desktop](https://claude.ai/download) (free)
- Git

### 1. Install uv (one time only)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repo

```bash
git clone https://github.com/yourusername/mood-journey-mcp.git
cd mood-journey-mcp
```

### 3. Install dependencies

```bash
uv sync
```

> `uv sync` reads `pyproject.toml`, creates a virtual environment, and installs everything automatically.

### 4. Configure Claude Desktop

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mood-journey": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/mood-journey-mcp/server.py"]
    }
  }
}
```

### 5. Restart Claude Desktop

You should see **mood-journey** appear in Claude's tool list (🔧 icon).

---

## 📦 Dependencies

Managed by `uv` via `pyproject.toml`:

```toml
[project]
name = "mood-journey-mcp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",           # MCP Python SDK
    "python-dotenv>=1.0.0", # Environment variable management
]
```

Add a new dependency:
```bash
uv add package-name
```

Run the server:
```bash
uv run server.py
```

> ✅ No external APIs. No database. Just Python + a JSON file.

---

## 📊 Mood Score Scale

| Score | Meaning | Emoji |
|-------|---------|-------|
| 1–2 | Very low / crisis | 😔 |
| 3–4 | Struggling | 😟 |
| 5–6 | Neutral / okay | 😐 |
| 7–8 | Good | 😊 |
| 9–10 | Excellent | 🌟 |

---

## 💬 Example Prompts

**Logging:**
- `"I'm feeling great today, just finished a big project!"`
- `"Log mood: tired and a bit stressed, score 4"`
- `"I feel calm and focused right now"`

**Checking in:**
- `"How have I been feeling this week?"`
- `"What was my mood like last Monday?"`
- `"Show me my happiest days this month"`

**Finding patterns:**
- `"Do I feel worse on certain days of the week?"`
- `"What words or situations come up when I feel anxious?"`
- `"How long does it usually take me to recover from a bad day?"`

**Streaks & goals:**
- `"How many days in a row have I logged my mood?"`
- `"Have I been more positive or negative this month vs last month?"`

---

## 🗺️ Roadmap

- [x] Phase 1: Project setup & Hello World MCP tool
- [x] Phase 2: `log_mood` + local JSON storage
- [x] Phase 3: `get_today` + `get_mood_summary`
- [ ] Phase 4: `find_patterns` — day/time/keyword analysis
- [ ] Phase 5: Mood streaks & consistency tracking
- [ ] Phase 6: `export_data` to CSV
- [ ] Phase 7: Emotion tag suggestions (auto-complete common tags)
- [ ] Phase 8: Weekly reflection prompt (Claude proactively summarizes)

---

## 🏗️ Architecture

```
┌──────────────────┐      MCP (stdio)      ┌──────────────────────┐
│  Claude Desktop  │ ◄───────────────────► │   server.py (MCP)    │
│  (AI client)     │   tool calls/results  │                      │
└──────────────────┘                       └──────────┬───────────┘
                                                      │
                                           ┌──────────▼───────────┐
                                           │   storage/db.py      │
                                           │   Read/Write JSON    │
                                           └──────────┬───────────┘
                                                      │
                                           ┌──────────▼───────────┐
                                           │   data/moods.json    │
                                           │   (local only)       │
                                           │   🔒 gitignored      │
                                           └──────────────────────┘
```

---

## 🗃️ Data Format

Your `moods.json` stores entries like this:

```json
{
  "entries": [
    {
      "id": "20250228-001",
      "timestamp": "2025-02-28T09:15:00",
      "score": 7,
      "emotion": "calm",
      "note": "Good morning, slept well",
      "day_of_week": "Friday"
    }
  ]
}
```

Plain, readable, portable. You own it completely.

---

## 🤝 Contributing

Ideas welcome! Areas that need help:
- Mood visualization (ASCII charts in terminal)
- Multiple user profiles
- Reminder system (log mood at set times)
- Integrations with Apple Health / Google Fit (optional, opt-in)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Built as a portfolio project demonstrating MCP server development with local-first data storage and conversational UX design.

---

## 💛 A Note

Mental health matters. This tool is meant to support self-reflection, not replace professional support. If you're struggling, please reach out to someone you trust or a mental health professional.
