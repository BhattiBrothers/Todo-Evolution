# [Spec: SPEC-001, SPEC-002, SPEC-003 — Phase II Entry Point]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_db_and_tables
from routes.tasks import router as tasks_router
from routes.chat import router as chat_router
from routes.subscriptions import router as subscriptions_router

app = FastAPI(title="Todo Evolution API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/health")
def health():
    return {"status": "ok", "phase": "II"}


app.include_router(tasks_router)
app.include_router(chat_router)
app.include_router(subscriptions_router)
