# Feature Spec: Task CRUD Operations
## Phase I — In-Memory Python Console App

**Spec ID:** SPEC-001  
**Phase:** I  
**Status:** Approved

---

## User Stories

- As a user, I can add a new task with a title and optional description
- As a user, I can view all my tasks with their status
- As a user, I can update a task's title or description
- As a user, I can delete a task by its ID
- As a user, I can mark a task as complete or incomplete

---

## Acceptance Criteria

### Feature 1: Add Task
- User provides a title (required, 1–200 characters)
- User optionally provides a description (max 1000 characters)
- System assigns a unique integer ID (auto-increment starting from 1)
- System sets `completed = False` and records `created_at` timestamp
- System confirms creation with task ID and title
- Error if title is empty or exceeds 200 characters

### Feature 2: View Task List
- Display all tasks in a formatted table
- Show: ID, Title, Description (truncated to 50 chars), Status ([ ] or [x]), Created date
- If no tasks exist, show: "No tasks found. Add one with 'add'."
- Tasks displayed in order of creation (oldest first)

### Feature 3: Update Task
- User provides task ID and new title and/or description
- System updates the specified fields only (partial update allowed)
- Error if task ID does not exist
- Error if new title is empty or exceeds 200 characters
- System confirms update with updated task details

### Feature 4: Delete Task
- User provides task ID
- System removes the task permanently from memory
- Error if task ID does not exist
- System confirms deletion with task title

### Feature 5: Mark as Complete / Incomplete
- User provides task ID
- System toggles `completed` status (True → False or False → True)
- Error if task ID does not exist
- System confirms with new status

---

## Domain Rules

- Task IDs are unique integers, never reused after deletion
- Tasks are stored in memory only (no file/database persistence)
- All data is lost when the program exits — this is expected behavior for Phase I
- A task must always have a title; description is optional

---

## Data Model

```
Task:
  id: int           # unique, auto-increment
  title: str        # required, max 200 chars
  description: str  # optional, max 1000 chars, default ""
  completed: bool   # default False
  created_at: str   # ISO format timestamp
```

---

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new task | `add` |
| `list` | View all tasks | `list` |
| `update <id>` | Update a task | `update 1` |
| `delete <id>` | Delete a task | `delete 2` |
| `complete <id>` | Toggle completion | `complete 3` |
| `help` | Show help menu | `help` |
| `quit` / `exit` | Exit the app | `quit` |

---

## UI/UX Requirements

- Clear prompts for user input
- Formatted table output for task list
- Color-coded status: incomplete = white, complete = green (if terminal supports it)
- Confirmation messages after every action
- Error messages must be descriptive (not just "Error")
- Help menu shows all available commands with descriptions
