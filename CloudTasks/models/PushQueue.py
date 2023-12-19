from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import Field

from ...base_types import JsonBase, JsonHTTPMethod

class TypeEnum(Enum):
    type_unspecified = "TYPE_UNSPECIFIED"
    pull = "PULL"
    push = "PUSH"

class InputStats(JsonBase):
    pass

class JsonPushQueueBase(JsonBase):
    """
    Model representing a GAE queue as json.
    https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues#resource:-queue
    """
    name: str
    """The name of the Push Queue.\n
    format: projects/kapi-development/locations/us-central1/queues/testq1
    """
    rate_limits: JsonRateLimits
    retry_config: JsonRetryConfig
    task_ttl: str = "864000s"
    tombstone_ttl: str = "3600s"
    stackdriver_logging_config: StackdriverLoggingConfig
    type_enum: TypeEnum = Field(default=TypeEnum.push, alias="type")


class JsonPushQueueInput(JsonPushQueueBase):
    http_target: JsonHTTPTarget
    app_engine_http_queue: JsonAppEngineHttpQueue
    stats: InputStats = InputStats()


class JsonPushQueueOutput(JsonPushQueueBase):
    state: State
    # purge_time: str
    # stats: QueueStats


class JsonAppEngineHttpQueue(JsonBase):
    app_engine_routing_override: JsonAppEngineRouting


class JsonAppEngineRouting(JsonBase):
    # service: str = ""
    # version: str = ""
    # instance: str = ""
    # host: str = ""
    pass


class QueueStats(JsonBase):
    tasks_count: str
    oldest_estimated_arrival_time: str
    executed_last_minute_count: str
    concurrent_dispatches_count: str
    effective_execution_rate: float


class StackdriverLoggingConfig(JsonBase):
    sampling_ratio: float = 1.0


class State(Enum):
    state_unspecified = "STATE_UNSPECIFIED"
    running = "RUNNING"
    paused = "PAUSED"
    disabled = "DISABLED"


class JsonRetryConfig(JsonBase):
    max_attempts: int = 100
    max_retry_duration: str = "0s"
    min_backoff: str = "0.1s"
    max_backoff: str = "3600s"
    max_doublings: int = 16


class JsonRateLimits(JsonBase):
    max_dispatches_per_second: float = 500.0
    max_burst_size: int = 500
    max_concurrent_dispatches: int = 1000


class JsonHTTPTarget(JsonBase):
    uri_override: JsonUriOverride
    http_method: JsonHTTPMethod
    header_overrides: List[JsonHeaderOverride] = []
    oidc_token: OidcToken


class OidcToken(JsonBase):
    service_account_email: str
    audience: str


class JsonHeaderOverride(JsonBase):
    header: JsonHeader


class JsonHeader(JsonBase):
    key: str
    value: str

class UriOverrideEnforceMode(Enum):
    uri_override_enforce_mode_unspecified = "URI_OVERRIDE_ENFORCE_MODE_UNSPECIFIED"
    if_not_exists = "IF_NOT_EXISTS"
    always = "ALWAYS"


class Scheme(Enum):
    scheme_unspecified = "SCHEME_UNSPECIFIED"
    http = "HTTP"
    https = "HTTPS"


class JsonUriOverride(JsonBase):
    path_override: JsonPathOverride
    query_override: JsonQueryOverride
    uri_override_enforce_mode: UriOverrideEnforceMode \
        = UriOverrideEnforceMode.uri_override_enforce_mode_unspecified
    scheme: Scheme = Scheme.scheme_unspecified
    host: Optional[str] = None
    """Use None if unspecificied"""
    port: Optional[str] = None
    """Use None if unspecificied"""


class JsonPathOverride(JsonBase):
    path: str = ""


class JsonQueryOverride(JsonBase):
    query_params: str = ""


JsonPushQueueInput.update_forward_refs()
JsonHTTPTarget.update_forward_refs()
JsonUriOverride.update_forward_refs()
JsonAppEngineHttpQueue.update_forward_refs()
JsonPushQueueOutput.update_forward_refs()
