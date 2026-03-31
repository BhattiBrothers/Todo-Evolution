# Phase I — In-Memory Python Console Todo App

## Setup

**Requirements:** Python 3.13+, UV

```bash
# Run the app
uv run python -m src.main
```

## Features

| Feature | Command | Example |
|---------|---------|---------|
| Add task | `add` | type `add` then enter title |
| List tasks | `list` | `list` |
| Update task | `update <id>` | `update 1` |
| Delete task | `delete <id>` | `delete 2` |
| Toggle complete | `complete <id>` | `complete 3` |
| Help | `help` | `help` |
| Exit | `quit` or `exit` | `quit` |

## Notes

- Tasks are stored in memory only — all data is lost on exit (Phase I expected behavior)
- Built using Spec-Driven Development with Claude Code
