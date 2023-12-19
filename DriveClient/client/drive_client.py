from __future__ import annotations
import json

from typing import Any, BinaryIO, Dict, Generator, Tuple, IO
from abc import ABC
import asyncio
import tempfile

import httpx
from httpx import Request, Response, AsyncClient

from ...auth import get_drive_oauth_token

class DriveAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers['Authorization'] = f"Bearer {self.token}"
        yield request

class IDriveClient(ABC):
    def __init__(self) -> None:
        token = get_drive_oauth_token()
        self.client = AsyncClient(
            base_url=f"https://www.googleapis.com/drive/v3",
            auth=DriveAuth(token) # type: ignore
        )

class DriveClient(IDriveClient):
    def __init__(self) -> None:
        token = get_drive_oauth_token()
        self.client = AsyncClient(
            base_url="https://www.googleapis.com/drive/v3",
            auth=DriveAuth(token) # type: ignore
        )

    async def get_about(self) -> Response:
        """
        This is a shitty health check.
        Print's a 200 message or else colin is in poor health :(.
        """
        params = {
            "fields": "*"
        }
        res = await self.client.get(
            url="/about",
            params=params
        )
        print(res)
        return res

    async def get_xlsx_file_binary(self, file_id: str) -> IO:
        url = f"/files/{file_id}"
        file_req_params = {
            "alt": "media"
        }
        file_res = await self.client.get(
            url=url,
            params=file_req_params
        )
        assert file_res.status_code == 200
        xlsx_file = tempfile.NamedTemporaryFile(mode='w+b', suffix='.xlsx', delete=False)
        xlsx_file.write(file_res.content)
        xlsx_file.seek(0)
        return xlsx_file.file

    async def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        url = f"/files/{file_id}"
        data_req_params = {
            "fields": "*"
        }
        data_req = await self.client.get(
            url=url,
            params=data_req_params
        )
        assert data_req.status_code == 200
        return data_req.json()

    async def get_xlsx_file(self, file_id: str) -> Tuple[IO, Dict[str, Any]]:
        """Creates a file as first return arg that must be deleted sorry.
        :param file_id: file to read into tempfile
        :return: Tuple of [file as IO, metadata as dict]
        """
        file_task = self.get_xlsx_file_binary(file_id)
        data_task = self.get_file_metadata(file_id)
        [fh, data] = await asyncio.gather(
            file_task,
            data_task
        )
        return fh, data

    async def calculate_file_using_aspose(self) -> BinaryIO:
        ...

    async def calculate_file_locally(self, file_path: str) -> BinaryIO:
        import subprocess
        res = subprocess.run(["open", file_path])
        print(res)
        res.check_returncode()
        ...

