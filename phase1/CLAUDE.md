# Phase I — Claude Code Instructions

## What This Is
In-memory Python console Todo app. Phase I of the "Evolution of Todo" hackathon project.

## How to Run
```bash
uv run python -m src.main
```

## Spec Reference
All features implemented from: `@specs/features/task-crud.md` (SPEC-001)

## Project Structure
- `src/models.py` — Task dataclass
- `src/storage.py` — In-memory TaskStore
- `src/cli.py` — Command handlers (add, list, update, delete, complete)
- `src/main.py` — REPL entry point

## Coding Rules
- Python 3.13+, type hints required
- No database, no file I/O — memory only
- Follow PEP 8
- Every change must reference a Spec section
