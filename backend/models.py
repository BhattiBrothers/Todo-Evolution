# [Spec: SPEC-003 — Database Schema]
# SQLModel database models for tasks

from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(SQLModel):
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None


class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
