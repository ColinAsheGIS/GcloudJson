from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from base_types import JsonBase, OidcToken

class SubscriptionBase(JsonBase):
    name: str
    topic: str
    ack_deadline_seconds: Optional[int]
    retain_acked_messages: Optional[bool]
    message_retention_duration: Optional[str]
    labels: Optional[Dict[str, str]]
    enable_message_ordering: Optional[bool]
    expiration_policy: Optional[ExpirationPolicy]
    filter: Optional[str]
    dead_letter_policy: Optional[DeadLetterPolicy]
    retry_policy: Optional[RetryPolicy]
    detached: Optional[bool]
    enable_exactly_once_delivery: Optional[bool]
    topic_message_retention_duration: Optional[str]
    state: Optional[SubscriptionState]

class SubscriptionState(Enum):
    state_unspecified = "STATE_UNSPECIFIED"
    active = "ACTIVE"
    resource_error = "RESOURCE_ERROR"

class ExpirationPolicy(JsonBase):
    ttl: Optional[str]

class DeadLetterPolicy(JsonBase):
    dead_letter_topic: Optional[str]
    max_delivery_attempts: Optional[int]

class RetryPolicy(JsonBase):
    minimum_backoff: Optional[str]
    maximum_backoff: Optional[str]

class PushConfigSubscription(SubscriptionBase):
    push_config: PushConfig

class PushConfig(JsonBase):
    push_endpoint: Optional[str]
    attributes: Optional[Dict[str, str]]
    oidc_token: Optional[OidcToken]
    """oidc tokens for use when making authenticated requests to private"""
    pubsub_wrapper: Optional[PubsubWrapper]
    no_wrapper: Optional[NoWrapper]

class NoWrapper(JsonBase):
    write_metadata: Optional[bool]

class PubsubWrapper(JsonBase):
    pass

class BigqueryConfigSubscription(SubscriptionBase):
    bigquery_config: BigQueryConfig

class BigQueryConfig(JsonBase):
    table: Optional[str]
    """Name of table to write data to"""
    use_topic_schema: Optional[bool]
    write_metadata: Optional[bool]
    drop_unknown_fields: Optional[bool]
    state: Optional[BQState]

class BQState(Enum):
    state_unspecified = "STATE_UNSPECIFIED"
    active = "ACTIVE"
    permission_denied = "PERMISSION_DENIED"
    not_found = "NOT_FOUND"
    schema_mismatch = "SCHEMA_MISMATCH"

class CloudStorageConfigSubscription(SubscriptionBase):
    cloud_storage_config: CloudStorageConfig

class CloudStorageConfig(JsonBase):
    bucket: str
    filename_prefix: Optional[str]
    filename_suffix: Optional[str]
    max_duration: Optional[str]
    max_bytes: int
    state: Optional[CloudStorageState]
    text_config: Optional[TextConfig]
    avro_config: Optional[AvroConfig]

class TextConfig(JsonBase):
    ...

class AvroConfig(JsonBase):
    write_metadata: Optional[bool]

class CloudStorageState(Enum):
    state_unspecified = "STATE_UNSPECIFIED"
    active = "ACTIVE"
    permission_denied = "PERMISSION_DENIED"
    not_found = "NOT_FOUND"

class APIConfigSubscription(SubscriptionBase):
    ...

class AckRequest(JsonBase):
    ack_ids: List[str]
