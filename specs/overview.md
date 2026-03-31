# Todo App — Project Overview

## Purpose
A todo application that evolves from a Python CLI tool to a cloud-native, AI-powered distributed system.

## Current Phase
Phase I: In-Memory Python Console App

## Tech Stack (Phase I)
- Language: Python 3.13+
- Package Manager: UV
- Storage: In-memory (Python list/dict)
- Interface: Command-line (interactive REPL)

## Features (Phase I)
- [x] Add Task
- [x] List Tasks
- [x] Update Task
- [x] Delete Task
- [x] Mark Complete/Incomplete

## Project Structure (Phase I)
```
phase1/
├── src/
│   ├── __init__.py
│   ├── main.py        # Entry point, REPL loop
│   ├── models.py      # Task dataclass/model
│   ├── storage.py     # In-memory task store
│   └── cli.py         # Command handlers
├── pyproject.toml
└── README.md
```
