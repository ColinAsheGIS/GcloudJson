from __future__ import annotations

from typing import Protocol

from httpx import AsyncClient

from cloud_tasks import JsonHTTPTarget, JsonPathOverride, create_default_http_target, create_default_push_queue_request, create_default_uri_override

class SupportsCreateQueue(Protocol):
    def create_queue(self) -> SupportsPushTask:
        ...

class SupportsPushTask(Protocol):
    def push_task(self) -> SupportsPushTask:
        ...

class PushQueue:
    def __init__(self) -> None:
        project_id = "kapi-development"
        location_id = "us-central1"
        self.client = AsyncClient(
            base_url="https://cloudtasks.googleapis.com/v2beta3/"
            f"projects/f{project_id}/locations/{location_id}/queues"
        )

    def create_queue(self) -> PushQueue:
        path_override = JsonPathOverride()
        query_override = JsonQueryOverride()
        http_target = JsonHTTPTarget()
        return self

if __name__ == '__main__':
    res = create_default_push_queue_request()
    print(res.json(by_alias=True))
