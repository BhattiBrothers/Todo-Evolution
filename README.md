# Evolution of Todo — Hackathon II

Spec-Driven Development project built with Claude Code and Spec-Kit Plus.

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Python Console App | ✅ Complete |
| II | Full-Stack Web App (Next.js + FastAPI) | 🔜 |
| III | AI Chatbot (OpenAI Agents SDK + MCP) | 🔜 |
| IV | Local Kubernetes (Minikube + Helm) | 🔜 |
| V | Cloud Deployment (Kafka + Dapr) | 🔜 |

## Development Approach

All code is generated via **Spec-Driven Development**:
1. Write spec in `/specs/features/`
2. Claude Code implements from spec
3. No manual coding

## Quick Start (Phase I)

```bash
cd phase1
uv run python -m src.main
```

## Project Structure

```
hackathon-todo/
├── AGENTS.md          # Constitution — project rules for all AI agents
├── CLAUDE.md          # Claude Code entry point
├── specs/             # All feature specifications
│   ├── features/      # What to build
│   └── overview.md    # Project overview
├── specs-history/     # Version history of specs
└── phase1/            # Phase I source code
    └── src/
```
