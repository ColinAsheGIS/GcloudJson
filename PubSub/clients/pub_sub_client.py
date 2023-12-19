from __future__ import annotations
from collections.abc import Callable

import typing
from typing import Any, Optional, Protocol, Union, List

import httpx
from httpx import AsyncClient, Request, Response

from ..models.pub_sub_topics import PubSubMessageRequest, PublishMessageBody, PublishToTopicResponse
from ...base_types import JsonBase

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

def wrap_message(dev_topic_msg: DevTopicMessage) -> PublishMessageMonad:
    import base64
    data = base64.b64encode(bytes(dev_topic_msg.json(by_alias=True), encoding='utf-8'))
    mm = MessageMonad(data=data)
    pmm = PublishMessageMonad(messages=[mm])
    return pmm


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
    project_id: str
    location_id: str
    def __init__(self) -> None:
        token: str = "abstract_token"
        self.client = AsyncClient(
            base_url="https://pubsub.googleapis.com/v1/"
                     f"projects/{self.project_id}/locations/{self.location_id}/topics/{self.topic_id}",
            auth=PubSubAuth(token),
        )

    def _wrap_message(self, message: JsonBase) -> str:
        b64_message = PubSubMessageRequest.from_json_base(message)
        req_body = PublishMessageBody(messages=[b64_message])
        return req_body.json(by_alias=True)

    async def publish_message(self, message: JsonBase) -> PublishToTopicResponse:
        res = await self.client.post(
            url=":publish",
            content=self._wrap_message(message)
        )
        assert res.status_code == 200
        message_ids_res = res.json()
        return PublishToTopicResponse(**message_ids_res)

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.aclose()

