# [Phase V — Dapr event subscriber]
# Receives task events from Kafka via Dapr pubsub

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["events"])

PUBSUB_NAME = "todo-pubsub"
TOPIC = "task-events"


@router.get("/dapr/subscribe")
def dapr_subscribe():
    """Tell Dapr which topics this app subscribes to."""
    return [
        {
            "pubsubname": PUBSUB_NAME,
            "topic": TOPIC,
            "route": "/events/task-events",
        }
    ]


class CloudEvent(BaseModel):
    data: dict = {}


@router.post("/events/task-events")
def handle_task_event(event: CloudEvent):
    """Handle incoming task events from Kafka via Dapr."""
    event_type = event.data.get("type", "unknown")
    task_id = event.data.get("task_id")
    print(f"[Dapr Event] {event_type} — task_id={task_id}")
    return {"status": "SUCCESS"}
