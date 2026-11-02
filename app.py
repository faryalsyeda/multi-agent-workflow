"""FastAPI demo for the Multi-Agent Workflow.

Run (after installing requirements):
    uvicorn app:app --reload

Try:
    POST /run
    {"topic": "lead generation", "audience": "small cafes"}

This file is optional for the portfolio demo. The core logic lives in
workflow.py and works with plain Python, no server needed.
"""

import os

from workflow import run_workflow

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover
    FastAPI = None
    BaseModel = object


if FastAPI is None:
    raise SystemExit("Install requirements first: pip install -r requirements.txt")

app = FastAPI(title="Multi-Agent Research and Outreach Workflow")

_DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")


class Task(BaseModel):
    topic: str = ""
    audience: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
def run_task(body: Task):
    return run_workflow(body.topic, body.audience, _DATA_DIR)
