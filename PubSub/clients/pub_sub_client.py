from __future__ import annotations
from collections.abc import Callable

import typing
from typing import Any, Optional, Protocol, Union

import httpx
from httpx import AsyncClient, Request, Response

from ...kaffeine import get_oauth_token
from ...kaffeine.settings import get_project_settings

from PubSub.models.pub_sub_topics import PublishToTopicResponse

class PbSafeProtocol(Protocol):
    def json(
            self,
            *,
            include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
            exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
            by_alias: bool = False,
            skip_defaults: Optional[bool] = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            encoder: Optional[Callable[[Any], Any]] = None,
            models_as_dict: bool = True,
            **dumps_kwargs: Any,
        ) -> str:
        ...

class PubSubAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers['Authorization'] = f"Bearer {self.token}"
        yield request

class SupportsPublishMessage(Protocol):
    async def publish_message(self, message: PbSafeProtocol) -> PublishToTopicResponse:
        ...

class IPublisherClient:
    topic_id: str
    def __init__(self) -> None:
        settings = get_project_settings(base_settings=True)
        project_id = settings.current_service # type: ignore
        location_id = "us-central1"
        token = get_oauth_token(scopes=['https://www.googleapis.com/auth/pubsub'])
        self.client = AsyncClient(
            base_url="https://pubsub.googleapis.com/v1/"
                     f"projects/{project_id}/locations/{location_id}/topics/{self.topic_id}",
            auth=PubSubAuth(token),
        )

    async def publish_message(self, message: PbSafeProtocol) -> PublishToTopicResponse:
        res = await self.client.post(
            url="",
            content=message.json(by_alias=True)
        )
        assert res.status_code == 200
        message_ids_res = res.json()
        return PublishToTopicResponse(**message_ids_res)

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.aclose()

