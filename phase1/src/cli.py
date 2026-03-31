# [Spec: SPEC-001, Section: CLI Commands + Acceptance Criteria]
# Command handlers for all 5 basic features

from src.storage import TaskStore
from src.models import Task

store = TaskStore()


def _print_table(tasks: list[Task]) -> None:
    if not tasks:
        print("\n  No tasks found. Add one with 'add'.\n")
        return

    header = f"  {'ID':<5} {'Status':<6} {'Title':<30} {'Description':<35} {'Created':<20}"
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for task in tasks:
        status = task.status_icon()
        title = task.title[:28] + ".." if len(task.title) > 30 else task.title
        created = task.created_at[:10]
        print(f"  {task.id:<5} {status:<6} {title:<30} {task.short_description():<35} {created:<20}")
    print("-" * len(header) + "\n")


def cmd_add() -> None:
    # [Spec: SPEC-001, Feature 1: Add Task]
    title = input("  Title (required): ").strip()
    if not title:
        print("  Error: Title cannot be empty.")
        return
    if len(title) > 200:
        print("  Error: Title must be 200 characters or less.")
        return

    description = input("  Description (optional, press Enter to skip): ").strip()
    if len(description) > 1000:
        print("  Error: Description must be 1000 characters or less.")
        return

    task = store.add(title=title, description=description)
    print(f"  Task #{task.id} added: \"{task.title}\"")


def cmd_list() -> None:
    # [Spec: SPEC-001, Feature 2: View Task List]
    tasks = store.get_all()
    _print_table(tasks)


def cmd_update(args: list[str]) -> None:
    # [Spec: SPEC-001, Feature 3: Update Task]
    if not args:
        print("  Usage: update <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  Error: Task ID must be a number.")
        return

    if store.get_by_id(task_id) is None:
        print(f"  Error: No task found with ID {task_id}.")
        return

    print(f"  Updating task #{task_id} (press Enter to keep current value):")
    current = store.get_by_id(task_id)
    print(f"  Current title: {current.title}")

    new_title = input("  New title: ").strip()
    new_description = input("  New description: ").strip()

    if new_title and len(new_title) > 200:
        print("  Error: Title must be 200 characters or less.")
        return

    task = store.update(
        task_id,
        title=new_title if new_title else None,
        description=new_description if new_description else None,
    )
    print(f"  Task #{task.id} updated: \"{task.title}\"")


def cmd_delete(args: list[str]) -> None:
    # [Spec: SPEC-001, Feature 4: Delete Task]
    if not args:
        print("  Usage: delete <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  Error: Task ID must be a number.")
        return

    task = store.delete(task_id)
    if task is None:
        print(f"  Error: No task found with ID {task_id}.")
        return

    print(f"  Task #{task_id} deleted: \"{task.title}\"")


def cmd_complete(args: list[str]) -> None:
    # [Spec: SPEC-001, Feature 5: Mark as Complete/Incomplete]
    if not args:
        print("  Usage: complete <id>")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print("  Error: Task ID must be a number.")
        return

    task = store.toggle_complete(task_id)
    if task is None:
        print(f"  Error: No task found with ID {task_id}.")
        return

    status = "complete" if task.completed else "incomplete"
    print(f"  Task #{task_id} marked as {status}: \"{task.title}\"")


def cmd_help() -> None:
    print("""
  ┌─────────────────────────────────────────────────────┐
  │                  Todo App — Commands                │
  ├──────────────┬──────────────────────────────────────┤
  │  add         │  Add a new task                      │
  │  list        │  View all tasks                      │
  │  update <id> │  Update a task's title/description   │
  │  delete <id> │  Delete a task by ID                 │
  │  complete <id>│ Toggle task completion status       │
  │  help        │  Show this help menu                 │
  │  quit / exit │  Exit the application                │
  └──────────────┴──────────────────────────────────────┘
""")
