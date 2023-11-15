from __future__ import annotations

from .Tasks import CreateHTTPTaskRequest, TaskBase

async def create_default_task_base(queue_id: str) -> TaskBase:
    task_base = TaskBase(
        name=f"{queue_id}/tasks",

    )
    ...

async def create_default_http_task() -> CreateHTTPTaskRequest:
    ...
