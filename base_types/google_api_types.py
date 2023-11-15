from __future__ import annotations

from datetime import datetime
from enum import Enum

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel
from pydantic.utils import to_lower_camel

def zulu_encode(dt: datetime) -> str:
    temp_stamp = Timestamp()
    temp_stamp.FromDatetime(dt)
    return temp_stamp.ToJsonString()

class JsonBase(BaseModel):

    class Config:
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return to_lower_camel(string)

        json_encoders = {
            datetime: zulu_encode
        }

class OidcToken(JsonBase):
    service_account_email: str
    audience: str

class JsonHTTPMethod(Enum):
    http_method_unspecified = "HTTP_METHOD_UNSPECIFIED"
    post = "POST"
    get = "GET"
    head = "HEAD"
    put = "PUT"
    delete = "DELETE"
    patch = "PATCH"
    options = "OPTIONS"

