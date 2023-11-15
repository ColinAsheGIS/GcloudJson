from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.utils import to_lower_camel

class JsonBase(BaseModel):
    class Config:
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return to_lower_camel(string)

class JsonHTTPMethod(Enum):
    http_method_unspecified = "HTTP_METHOD_UNSPECIFIED"
    post = "POST"
    get = "GET"
    head = "HEAD"
    put = "PUT"
    delete = "DELETE"
    patch = "PATCH"
    options = "OPTIONS"


