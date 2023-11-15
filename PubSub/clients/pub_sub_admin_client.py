from __future__ import annotations
from collections.abc import Callable

import typing
from typing import Any, Optional, Protocol, Union

import httpx
from httpx import AsyncClient, Request, Response

from ...kaffeine import get_oauth_token
from ...kaffeine.settings import get_project_settings

from PubSub.models.pub_sub_types import SchemaView
from PubSub.models.pub_sub_topics import TopicBase
from PubSub.models.pub_sub_schemas import SchemaInput, SchemaOutput

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

class IPubSubAdmin:
    def __init__(self) -> None:
        settings = get_project_settings(base_settings=True)
        project_id = settings.current_service # type: ignore
        location_id = "us-central1"
        token = get_oauth_token(scopes=['https://www.googleapis.com/auth/pubsub'])
        self.client = AsyncClient(
            base_url="https://pubsub.googleapis.com/v1/"
                     f"projects/{project_id}/locations/{location_id}/",
            auth=PubSubAuth(token),
        )

    async def create_schema(self, schema: SchemaInput, schema_id: str) -> SchemaOutput:
        content = schema.json(by_alias=True)
        res = await self.client.post(
            url="schemas",
            content=content,
            params={"schema_id": schema_id}
        )
        assert res.status_code == 200
        return SchemaOutput(**res.json())

    async def get_schema(self, schema_name: str, schema_view: SchemaView) -> SchemaOutput:
        res = await self.client.get(
            url=f"schemas/{schema_name}",
            params={"view": schema_view.value}
        )
        assert res.status_code == 200
        return SchemaOutput(**res.json())

    async def create_topic(self, topic: TopicBase) -> TopicBase:
        content = topic.json(exclude={"name"}, by_alias=True, exclude_unset=True)
        res = await self.client.put(
            url=f"topics/{topic.name}",
            content=content
        )
        assert res.status_code == 200
        return TopicBase(**res.json())

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.aclose()

