from __future__ import annotations
from datetime import datetime

from enum import Enum
from typing import Dict, List

from pydantic import validator

from base_types import JsonBase, JsonHTTPMethod

class View(Enum):
    view_unspecified = "VIEW_UNSPECIFIED"
    basic = "BASIC"
    full = "FULL"

class TaskBase(JsonBase):
    name: str
    schedule_time: str
    dispatch_deadline: str
    dispatch_count: int
    response_count: int
    first_attempt: Attempt
    last_attempt: Attempt
    view: View = View.view_unspecified

    @validator('schedule_time')
    def make_timestamp_str(cls, val) -> str:
        if isinstance(val, str):
            return val
        if isinstance(val, datetime):
            return val.isoformat()
        raise ValueError("Date or str")


class Attempt(JsonBase):
    schedule_time: str
    dispatch_time: str
    response_time: str
    response_status: Status

class Status(JsonBase):
    code: int
    message: str
    details: List[Dict]

class HttpRequest(JsonBase):
    url: str
    http_method: JsonHTTPMethod
    headers: Dict[str, str] = {}

class HTTPTask(TaskBase):
    http_request: HttpRequest

class CreateHTTPTaskRequest(JsonBase):
    task: HTTPTask
    response_view: View = View.view_unspecified

class AppEngineTask(TaskBase):
    ...

class PullMessageTask(TaskBase):
    ...
