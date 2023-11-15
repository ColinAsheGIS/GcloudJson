from __future__ import annotations

import typing
from typing import Protocol

import httpx
from httpx import AsyncClient, Request, Response

from CloudTasks import CreateHTTPTaskRequest, JsonPushQueueOutput, create_default_push_queue_request


class SupportsCreateQueue(Protocol):
    def create_queue(self, queue_name: str) -> SupportsPushTask:
        ...


class SupportsPushTask(Protocol):
    def push_task(self) -> SupportsPushTask:
        ...

class TasksAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers['Authorization'] = f"Bearer {self.token}"
        yield request

class TasksException(Exception):
    ...

class QueueDoesNotExistException(Exception):
    ...

class PushQueue:
    def __init__(self, queue_id: str) -> None:
        self.queue_id = queue_id
        settings = get_project_settings(base_settings=True)
        project_id = settings.current_service # type: ignore
        location_id = "us-central1"
        token = get_oauth_token(scopes=['https://www.googleapis.com/auth/cloud-tasks'])
        self.client = AsyncClient(
            base_url="https://cloudtasks.googleapis.com/v2beta3/"
                     f"projects/{project_id}/locations/{location_id}/queues",
            auth=TasksAuth(token),
        )

    async def __aenter__(self):
        await self.get_or_create_queue()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.aclose()

    async def close(self):
        await self.client.aclose()

    async def get_or_create_queue(self) -> PushQueue:
        try:
            await self.get_queue()
        except Exception:
            await self.create_queue()
        return self

    @property
    def json_queue(self) -> JsonPushQueueOutput:
        if self._json_queue is None:
            raise AttributeError("JSON Queue hasn't been set for PushQueue yet.")
        return self._json_queue

    @json_queue.setter
    def json_queue(self, val: JsonPushQueueOutput):
        self._json_queue = val

    @property
    def queue_id(self) -> str:
        return self._queue_id

    @queue_id.setter
    def queue_id(self, val: str):
        self._queue_id = val

    async def create_queue(self) -> PushQueue:
        push_queue_request = await create_default_push_queue_request(self.queue_id)
        data = push_queue_request.json(by_alias=True)
        res = await self.client.post(
            url="",
            content=data
        )
        if res.status_code != 200:
            raise TasksException(f"Error creating queue: {res.text}")
        self.json_queue = JsonPushQueueOutput(**res.json())
        return self

    async def get_queue(self) -> PushQueue:
        res = await self.client.get(
            url=f"{self.queue_id}"
        )
        if res.status_code == 404:
            raise QueueDoesNotExistException()
        if res.status_code != 200:
            raise TasksException(f"Error getting queue: {res.text}")
        self.json_queue = JsonPushQueueOutput(**res.json())
        return self

    async def delete_queue(self) -> bool:
        res = await self.client.delete(
            url=f"{self.queue_id}"
        )
        if res.status_code != 200:
            raise TasksException(f"Error deleting queue: {res.text}")
        return True

    async def create_task(self, task: CreateHTTPTaskRequest):
        data = task.json(by_alias=True)
        res = await self.client.post(
            url=f"{self.queue_id}",
            content=data
        )
        if res.status_code != 200:
            raise TasksException(f"Error creating task: {res.text}")
        res_task = res.json()
        print(res_task)
        return "Hey"

async def main():
    async with PushQueue("badq1") as task_session:
        print(task_session.json_queue)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
