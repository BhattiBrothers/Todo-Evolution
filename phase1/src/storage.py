# [Spec: SPEC-001, Section: Domain Rules]
# In-memory task store — all data lost on exit (Phase I expected behavior)

from src.models import Task


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def get_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def update(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        return task

    def delete(self, task_id: int) -> Task | None:
        return self._tasks.pop(task_id, None)

    def toggle_complete(self, task_id: int) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.completed = not task.completed
        return task
