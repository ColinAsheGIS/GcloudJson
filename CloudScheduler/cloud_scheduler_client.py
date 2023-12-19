from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from base64 import b64encode
import json

from typing import Any, Dict, Optional, Protocol, Union, List, Generator
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, validator
from pydantic.utils import to_lower_camel
from google.protobuf.timestamp_pb2 import Timestamp
from httpx import Auth, AsyncClient, Response, Request

from google_http.auth import get_scheduler_oauth_token


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


class RetryConfig(JsonBase):
    retry_count: int = 0
    max_retry_duration: str = "15s"
    min_backoff_duration: str = "3.5s"
    max_backoff_duration: str = "3.5s"
    max_doublings: int = 5


class HttpMethod(Enum):
    post = "POST"
    get = "GET"
    head = "HEAD"
    put = "PUT"
    delete = "DELETE"
    patch = "PATCH"
    options = "OPTIONS"


class AppEngineRouting(JsonBase):
    service: Optional[str]
    version: Optional[str]
    instance: Optional[str]
    host: Optional[str]


class AppEngineHttpTarget(JsonBase):
    http_method: HttpMethod
    app_engine_routing: Optional[AppEngineRouting] = None
    relative_uri: str
    headers: Dict[str, str]
    body: Union[bytes, str, Dict[str, Any]]

    @validator('body')
    def encode_body(cls, val: Union[Dict[str, Any], bytes, str]) -> bytes:
        if isinstance(val, Dict):
            val = json.dumps(val)
        if isinstance(val, str):
            val = b64encode(bytes(val, "utf-8"))
        return val


class CronJobBase(JsonBase):
    schedule: str = "0 8 */10 * *"  # defaults to every 10 days at 8am
    retry_config: RetryConfig
    attempt_deadline: Optional[str] = None
    app_engine_http_target: AppEngineHttpTarget


class CronJobCreate(CronJobBase):
    ...


class CronJobRead(CronJobBase):
    name: str
    description: Optional[str]
    time_zone: str  # Something like zoneinfo
    user_update_time: datetime
    state: str  # TODO: Use state enum
    status: Optional[str]  # TODO: use status enum
    schedule_time: Optional[datetime]
    last_attempt_time: Optional[datetime]


class ICloudSchedulerAuth(Auth):
    def __init__(self) -> None:
        super().__init__()

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers['Authorization'] = f"Bearer {self.token}"
        yield request

    @property
    @abstractmethod
    def token(self) -> str:
        raise NotImplementedError(
            "Token property must be implemented by subclass."
        )


class SupportsCreateJob(Protocol):
    async def create_job(self, cron_job_create: CronJobCreate) -> CronJobRead:
        ...


class MinimalCreateJob(BaseModel):
    relative_uri: str
    http_method: HttpMethod
    body: Optional[BaseModel]


class ICloudSchedulerClient(ABC):
    project_id: str
    location_id: str
    auth: Auth

    def __init__(self) -> None:
        self.client = AsyncClient(
            base_url="https://cloudscheduler.googleapis.com/v1beta1/"
            f"projects/{self.project_id}/locations/{self.location_id}/jobs",
            auth=self.auth
        )

    def _build_request(self, create_job: MinimalCreateJob) -> CronJobCreate:
        retry_config = RetryConfig()
        http_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        http_target = AppEngineHttpTarget(
            http_method=create_job.http_method,
            relative_uri=create_job.relative_uri,
            headers=http_headers,
            body=create_job.body.dict(
                exclude_unset=True, by_alias=True) if create_job.body else ""
        )
        cron_job = CronJobCreate(
            retry_config=retry_config,
            app_engine_http_target=http_target
        )
        return cron_job

    async def create_job(self, create_job: MinimalCreateJob) -> CronJobRead:
        cron_job = self._build_request(create_job)
        res = await self.client.post(
            url="",
            content=cron_job.json(by_alias=True, exclude_none=True)
        )
        print(res.text)
        return CronJobRead(**res.json())

    async def __aenter__(self) -> ICloudSchedulerClient:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self.client.aclose()


class ExampleAuth(ICloudSchedulerAuth):
    @property
    def token(self) -> str:
        return get_scheduler_oauth_token()


class ExampleScheduler(ICloudSchedulerClient):
    project_id = "colndev-405100"
    location_id = "us-east1"
    auth = ExampleAuth()


class ExampleRequest(JsonBase):
    dev_log: str


async def main():
    async with ExampleScheduler() as scheduler:
        ex_req = ExampleRequest(dev_log="From the python script!")
        job = MinimalCreateJob(
            relative_uri="/print_something",
            http_method=HttpMethod.post,
            body=ex_req
        )
        res = await scheduler.create_job(job)
        print(res)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
