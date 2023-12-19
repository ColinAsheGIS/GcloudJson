from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Coroutine, Generator, Optional, Protocol, Type
from datetime import datetime
import json
import os

import httpx
from httpx import AsyncClient, Request, Response
from google.cloud import secretmanager
from psycopg import Connection
from psycopg.conninfo import make_conninfo

from ...auth import get_sql_oauth_token
from ...base_types import zulu_encode, JsonBase, GCloudSettings
from ..models import SqlConnection


class SupportsAuthFlow(Protocol):
    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        ...


class SQLConnectionInfo(JsonBase):
    db_user: str
    db_password: str
    db_name: str


class _ICloudSqlClient(ABC):
    def __init__(self, instance: str) -> None:
        self.instance = instance
        token = get_sql_oauth_token()
        self.client = AsyncClient(
            base_url=f"https://sqladmin.googleapis.com/v1/"
            f"projects/{self.project_id}/instances/{self.instance}",
            auth=SqlAuth(token)  # type: ignore
        )

    def make_psyco_connection(self) -> Coroutine[None, None, Connection]:
        ...

    @property
    @abstractmethod
    def project_settings(self) -> GCloudSettings:
        raise NotImplementedError(
            f"Project settings must be set on classes "
            f"inheriting from ICloudSqlClient"
        )

    @property
    @abstractmethod
    def sql_connection_info(self) -> SQLConnectionInfo:
        raise NotImplementedError("")

    @property
    def project_id(self) -> str:
        return self.project_settings.project_id


class ColnDevCloudSQL(_ICloudSqlClient):
    @property
    def project_settings(self) -> GCloudSettings:
        return GCloudSettings(
            project_id='colndev-405100'
        )


class ICloudSQLClient(ABC):
    def __init__(self) -> None:
        self.client = AsyncClient(
            base_url=f"https://sqladmin.googleapis.com/v1/"
            f"projects/{self.project_id}/instances/{self.instance}",
            auth=self.auth_class  # type: ignore
        )

    @property
    @abstractmethod
    def auth_class(self) -> SupportsAuthFlow:
        ...

    @property
    @abstractmethod
    def project_id(self) -> str:
        ...

    @property
    @abstractmethod
    def instance(self) -> str:
        ...

    @property
    @abstractmethod
    def region(self) -> str:
        ...

    @abstractmethod
    def get_database_secrets(self, secret_name: str) -> SQLConnectionInfo:
        ...

    async def connect_unix_socket(self) -> Coroutine[None, None, Connection]:
        db_secrets = self.get_database_secrets("postgres_admin")
        unix_socket_path = f"/cloudsql/{self.project_id}:{
            self.region}:{self.instance}"
        if os.environ.get("USE_PROXY", None):
            unix_socket_path = 'localhost'
        conn_info = make_conninfo(
            # database='postgresql',
            user=db_secrets.db_user,
            password=db_secrets.db_password,
            dbname=db_secrets.db_name,
            host=unix_socket_path,
        )
        psyco_connection = Connection.connect(conn_info)
        return psyco_connection

    async def get_connection(self, read_time: Optional[datetime] = None) -> Coroutine[None, None, SqlConnection]:
        """
        Gets the connection values for a CloudSQL instance.
        :param read_time: Optional query param time for snapshot of db at that time.
        :return: SqlConnection
        """
        params = {"readTime": zulu_encode(read_time)} if read_time else None
        res = await self.client.get(
            url="/connectSettings",
            params=params
        )
        assert res.status_code == 200
        sql_conn = SqlConnection(**res.json())
        await self.connect_unix_socket()
        return sql_conn

    async def __aenter__(self) -> CloudSQLClient:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.aclose()
