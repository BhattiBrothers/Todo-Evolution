# [Spec: SPEC-001 + SPEC-002 — Task CRUD + Auth]
# Task API routes — all protected by JWT

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Task, TaskCreate, TaskUpdate, TaskRead
from auth import get_current_user
from events import publish_event

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


def _verify_ownership(user_id: str, current_user: str) -> None:
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access forbidden")


@router.get("", response_model=list[TaskRead])
def list_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    _verify_ownership(user_id, current_user)
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@router.post("", response_model=TaskRead, status_code=201)
def create_task(
    user_id: str,
    body: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    _verify_ownership(user_id, current_user)
    task = Task(user_id=user_id, title=body.title, description=body.description)
    session.add(task)
    session.commit()
    session.refresh(task)
    publish_event("task.created", {"task_id": task.id, "title": task.title, "user_id": user_id})
    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    _verify_ownership(user_id, current_user)
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: int,
    body: TaskUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    _verify_ownership(user_id, current_user)
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    if body.title is not None:
        task.title = body.title
    if body.description is not None:
        task.description = body.description
    if body.completed is not None:
        task.completed = body.completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    _verify_ownership(user_id, current_user)
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()


@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    _verify_ownership(user_id, current_user)
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
