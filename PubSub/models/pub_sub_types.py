from __future__ import annotations
from datetime import datetime

from enum import Enum
from typing import Dict, List, Optional

from pydantic import validator

from ...base_types import JsonBase


class PolicyVersion(Enum):
    pv_0 = 0
    pv_1 = 1
    pv_3 = 3

class GetPolicyOptions(JsonBase):
    """
    https://cloud.google.com/pubsub/docs/reference/rest/v1/GetPolicyOptions
    """
    requested_policy_version: Optional[PolicyVersion]
    """Optional. The maximum policy version that will be used to format the policy."""

class Policy(JsonBase):
    """
    https://cloud.google.com/pubsub/docs/reference/rest/v1/Policy
    """
    version: Optional[PolicyVersion]
    """Specifies the format of the policy."""
    bindings: List[Binding]
    etag: Optional[str]

class Binding(JsonBase):
    role: str
    members: List[str]
    """
    TODO: Needs special handlings
    """
    condition: Expr

class Expr(JsonBase):
    """
    This a whole language bruh
    """
    expression: str
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]

class PubsubMessage(JsonBase):
    data: Optional[str]
    attributes: Optional[Dict[str, str]]
    message_id: Optional[str]
    publish_time: Optional[datetime]
    ordering_key: Optional[str]

class SchemaView(Enum):
    schema_view_unspecified = "SCHEMA_VIEW_UNSPECIFIED"
    basic = "BASIC"
    full = "FULL"

class StreamingPullRequest(JsonBase):
    subscription: str
    ack_ids: Optional[List[str]]
    modify_deadline_seconds: Optional[List[int]]
    modify_deadline_ack_ids: Optional[List[int]]
    stream_ack_deadline_seconds: int
    client_id: Optional[str]
    max_outstanding_messages: Optional[str]
    max_outstanding_bytes: Optional[str]

    @validator('stream_ack_deadline_seconds')
    def ack_deadline_seconds(cls, val: int) -> int:
        if val < 10:
            raise ValueError(f"Ack deadline of {val} too short. (< 10s)")
        if val > 600:
            raise ValueError(f"Ack deadline of {val} too long. (< 600s)")
        return val

class StreamingPullResponse(JsonBase):
    received_message: Optional[List[ReceivedMessage]]
    acknowledge_confirmation: Optional[AcknowledgeConfirmation]
    modify_ack_deadline_confirmation: Optional[ModifyAckDeadlineConfirmation]
    subscription_properties: Optional[SubscriptionProperties]

class ReceivedMessage(JsonBase):
    ack_id: Optional[str]
    message: PubsubMessage
    delivery_attempt: int

class AcknowledgeBase(JsonBase):
    ack_ids: Optional[List[str]]
    invalid_ack_ids: Optional[List[str]]
    unordered_ack_ids: Optional[List[str]]

class AcknowledgeConfirmation(AcknowledgeBase):
    temporary_failed_ack_ids: Optional[List[str]]

class ModifyAckDeadlineConfirmation(AcknowledgeBase):
    pass

class SubscriptionProperties(JsonBase):
    exactly_once_delivery_enabled: Optional[bool]
    message_ordering_enabled: Optional[bool]

class TestIamPermissionsResponse(JsonBase):
    permissions: List[str]
