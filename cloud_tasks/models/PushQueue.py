from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic.utils import to_lower_camel

class JsonBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        @classmethod
        def alias_generator(cls, string: str) -> str:
            return to_lower_camel(string)

class TypeEnum(Enum):
    type_unspecified = "TYPE_UNSPECIFIED"
    pull = "PULL"
    push = "PUSH"

class JsonPushQueueInput(JsonBase):
    """
    Model representing a GAE queue as json.
    https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues#resource:-queue
    """
    name: str
    """The name of the Push Queue"""
    http_target: JsonHTTPTarget
    rate_limits: JsonRateLimits
    retry_config: JsonRetryConfig
    task_ttl: str = "3600s"
    tombstone_ttl: str = "3600s"
    stackdriver_logging_config: StackdriverLoggingConfig
    type_enum: TypeEnum = TypeEnum.push
    app_engine_http_queue: Optional[JsonAppEngineHttpQueue] = None

class JsonPushQueueOutput(JsonPushQueueInput):
    state: State
    purge_time: str
    stats: QueueStats

class JsonAppEngineHttpQueue(BaseModel):
    app_engine_routing_override: JsonAppEngineRouting 

class JsonAppEngineRouting(BaseModel):
    service: str
    version: str
    instance: str
    host: str

class QueueStats(JsonBase):
    tasksCount: str 
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
    max_retry_duration: str = "0" 
    min_backoff: str = "0.1"
    max_backoff: str = "3600"
    max_doublings: int = 16

class JsonRateLimits(JsonBase):
    max_dispatches_per_second: float = 500.0
    max_burst_size: int = 500
    max_concurrent_dispatches: int = 1000

class JsonHTTPTarget(JsonBase):
    uri_override: JsonUriOverride 
    http_method: JsonHTTPMethod
    header_overrides: List[JsonHeaderOverride] 
    oidc_token: OidcToken 

class OidcToken(JsonBase):
    service_account_email: str
    scope: str

class JsonHeaderOverride(JsonBase):
    header: JsonHeader

class JsonHeader(JsonBase):
    key: str
    value: str

class JsonHTTPMethod(Enum):
    http_method_unspecified = "HTTP_METHOD_UNSPECIFIED"
    post = "POST"
    get = "GET"
    head = "HEAD"
    put = "PUT"
    delete = "DELETE"
    patch = "PATCH"
    options = "OPTIONS"

class JsonUriOverride(JsonBase):
    path_override: JsonPathOverride 
    query_override: JsonQueryOverride 
    uri_override_enforce_mode: UriOverrideEnforceMode 
    scheme: Scheme 
    host: str
    port: str

class JsonPathOverride(JsonBase):
    path: str

class JsonQueryOverride(JsonBase):
    query_params: str

class UriOverrideEnforceMode(Enum):
    uri_override_enforce_mode_unspecified = "URI_OVERRIDE_ENFORCE_MODE_UNSPECIFIED"
    if_not_exists = "IF_NOT_EXISTS"
    always = "ALWAYS"

class Scheme(Enum):
    scheme_unspecified = "SCHEME_UNSPECIFIED"
    http = "HTTP"
    https = "HTTPS"

JsonPushQueueInput.update_forward_refs()
JsonHTTPTarget.update_forward_refs()
JsonUriOverride.update_forward_refs()
