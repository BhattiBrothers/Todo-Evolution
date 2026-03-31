# [Spec: SPEC-001, Section: Data Model]
# Task dataclass — in-memory representation of a todo item

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def status_icon(self) -> str:
        return "[x]" if self.completed else "[ ]"

    def short_description(self) -> str:
        if len(self.description) > 50:
            return self.description[:47] + "..."
        return self.description or "-"
