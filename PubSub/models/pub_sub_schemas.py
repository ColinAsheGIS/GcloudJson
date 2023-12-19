from __future__ import annotations
from datetime import datetime

from enum import Enum

from pydantic import Field

from ...base_types import JsonBase

class SchemaType(Enum):
    type_unspecified = "TYPE_UNSPECIFIED"
    protocol_buffer = "PROTOCOL_BUFFER"
    avro = "AVRO"

class SchemaInput(JsonBase):
    name: str
    schema_type: SchemaType = Field(alias="type", default=SchemaType.avro)
    definition: str

class SchemaOutput(SchemaInput):
    revision_id: str
    revision_create_time: datetime

