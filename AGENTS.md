# AGENTS.md — Hackathon II: Evolution of Todo
## Constitution (The Brain)

This project uses **Spec-Driven Development (SDD)** — no agent is allowed to write code
until the specification is complete and approved.

All AI agents must follow the **Spec-Kit lifecycle**:
> **Specify → Plan → Tasks → Implement**

---

## Project Overview

**Name:** Evolution of Todo  
**Goal:** Build a Todo app that evolves from a Python CLI tool to a cloud-native AI chatbot  
**Developer:** Umer Bhatti  
**Stack evolution:** Python Console → Next.js + FastAPI → AI Chatbot → Kubernetes → Kafka + Dapr

---

## Tech Stack (By Phase)

| Phase | Stack |
|-------|-------|
| I | Python 3.13+, UV, in-memory storage |
| II | Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth |
| III | OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK |
| IV | Docker, Minikube, Helm, kubectl-ai, kagent |
| V | Kafka, Dapr, AKS/GKE/OKE |

---

## Coding Standards (Non-Negotiables)

1. **Python:** Use Python 3.13+, managed with UV
2. **No manual code:** All code generated via Claude Code from specs
3. **Type hints:** All functions must have type annotations
4. **Clean code:** Follow PEP 8, meaningful variable names
5. **No hardcoded values:** Use constants or config
6. **Error handling:** Graceful errors at all user-facing boundaries

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Spec section.**
2. **Never modify architecture without updating `speckit.plan`.**
3. **Never propose features without a spec in `/specs/features/`.**
4. **Every implementation must map back to a spec.**
5. **If spec is ambiguous, stop and request clarification.**

**Conflict resolution hierarchy:** Constitution > Specify > Plan > Tasks

---

## Spec-Kit Workflow

### 1. Constitution (WHY — Principles & Constraints)
File: `AGENTS.md`  
Non-negotiables: architecture values, tech stack, coding standards.

### 2. Specify (WHAT — Requirements & Acceptance Criteria)
Files: `/specs/features/*.md`  
User stories, acceptance criteria, domain rules.

### 3. Plan (HOW — Architecture & Components)
Files: `/specs/overview.md`, `/specs/architecture.md`  
Component breakdown, API design, data flow.

### 4. Tasks (BREAKDOWN — Atomic Work Units)
Each task must have: Task ID, description, preconditions, expected output.

### 5. Implement (CODE — Only What Tasks Authorize)
Reference Task IDs. Follow the plan exactly. No improvisation.

---

## Agent Failure Modes (MUST AVOID)

- Freestyle code without specs
- Adding features not in spec
- Ignoring acceptance criteria
- Creating architecture not in plan

---

## Project Structure

```
hackathon-todo/
├── AGENTS.md              # This file — Constitution
├── CLAUDE.md              # Claude Code entry point
├── .spec-kit/
│   └── config.yaml        # Spec-Kit configuration
├── specs/
│   ├── overview.md        # Project overview
│   ├── architecture.md    # System architecture
│   ├── features/          # Feature specs (WHAT)
│   ├── api/               # API specs
│   ├── database/          # Schema specs
│   └── ui/                # UI specs
├── specs-history/         # All previous spec versions
├── phase1/                # Phase I: Python console app
├── frontend/              # Phase II+: Next.js
├── backend/               # Phase II+: FastAPI
└── README.md
```
