from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional
import base64

from pydantic.fields import Field

from ...base_types import JsonBase

class TopicBase(JsonBase):
    name: str
    labels: Optional[Dict[str, str]]
    message_storage_policy: Optional[MessageStoragePolicy]
    kms_key_name: Optional[str]
    schema_settings: Optional[SchemaSettings]
    satisfies_pzs: Optional[bool]
    message_retention_duration: Optional[str]

class MessageStoragePolicy(JsonBase):
    allowed_persistence_regions: Optional[List[str]]

class SchemaSettings(JsonBase):
    schema_: str = Field(alias="schema")
    encoding: Encoding
    first_revision_id: Optional[str]
    last_revision_id: Optional[str]

class Encoding(Enum):
    encoding_unspecified = "ENCODING_UNSPECIFIED"
    json = "JSON"
    binary = "BINARY"

class PublishToTopicResponse(JsonBase):
    message_ids: Optional[List[str]]

class PubSubMessageRequest(JsonBase):
    data: bytes
    @classmethod
    def from_json_base(cls, instance: JsonBase) -> PubSubMessageRequest:
        as_bytes = bytes(
            instance.json(by_alias=True), encoding="utf-8"
        )
        as_b64 = base64.b64encode(as_bytes)
        return PubSubMessageRequest(data=as_b64)

class PublishMessageBody(JsonBase):
    messages: List[PubSubMessageRequest]

TopicBase.update_forward_refs()

