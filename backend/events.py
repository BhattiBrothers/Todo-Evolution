# [Phase V — Dapr event publishing]
# Publishes task events to Kafka via Dapr pubsub sidecar

import os
import httpx

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
PUBSUB_NAME = "todo-pubsub"
TOPIC = "task-events"


def publish_event(event_type: str, payload: dict) -> None:
    """Fire-and-forget event publish via Dapr sidecar."""
    try:
        url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/{TOPIC}"
        data = {"type": event_type, **payload}
        httpx.post(url, json=data, timeout=2.0)
    except Exception:
        pass  # Non-blocking — don't fail the main request if Dapr isn't running
