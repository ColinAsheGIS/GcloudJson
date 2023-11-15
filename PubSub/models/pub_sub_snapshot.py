from __future__ import annotations
from datetime import datetime

from typing import List, Optional

from base_types import JsonBase

class SnapshotBase(JsonBase):
    name: Optional[str]
    topic: Optional[str]
    expire_time: datetime
    labels: List[str]

class _:
    ...

