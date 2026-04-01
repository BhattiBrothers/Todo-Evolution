# [Spec: SPEC-003 — Phase III AI Chatbot]
# Chat endpoint with Groq function calling — manages tasks via AI

import json
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from groq import Groq
from db import get_session
from models import Task, TaskCreate
from auth import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the current user",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description", "default": ""},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_complete",
            "description": "Toggle a task's completion status",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task to toggle"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task to delete"},
                },
                "required": ["task_id"],
            },
        },
    },
]


def _execute_tool(name: str, args: dict, user_id: str, session: Session) -> str:
    if name == "list_tasks":
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        if not tasks:
            return "No tasks found."
        lines = [f"- [{t.id}] {'✓' if t.completed else '○'} {t.title}" for t in tasks]
        return "\n".join(lines)

    elif name == "create_task":
        task = Task(
            user_id=user_id,
            title=args["title"],
            description=args.get("description", ""),
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return f"Task created: [{task.id}] {task.title}"

    elif name == "toggle_complete":
        task = session.get(Task, args["task_id"])
        if not task or task.user_id != user_id:
            return f"Task {args['task_id']} not found."
        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        status = "completed" if task.completed else "incomplete"
        return f"Task [{task.id}] marked as {status}."

    elif name == "delete_task":
        task = session.get(Task, args["task_id"])
        if not task or task.user_id != user_id:
            return f"Task {args['task_id']} not found."
        session.delete(task)
        session.commit()
        return f"Task [{args['task_id']}] deleted."

    return "Unknown tool."


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    reply: str


@router.post("", response_model=ChatResponse)
def chat(
    user_id: str,
    body: ChatRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access forbidden")

    system = (
        "You are a helpful todo assistant. You can list, create, complete, and delete tasks "
        "for the user. Use the provided tools to manage their tasks. Be concise and friendly."
    )

    messages = [{"role": "system", "content": system}]
    messages.extend(body.history[-10:])  # keep last 10 messages for context
    messages.append({"role": "user", "content": body.message})

    # Agentic loop — keep calling until no more tool calls
    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return ChatResponse(reply=msg.content or "")

        # Convert response object to dict for next iteration
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        })
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = _execute_tool(tc.function.name, args, user_id, session)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    return ChatResponse(reply="Sorry, I couldn't complete that request.")
