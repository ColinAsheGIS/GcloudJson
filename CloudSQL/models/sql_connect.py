from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from ...base_types import JsonBase

class SqlConnection(JsonBase):
    kind: str = "sql#connectSettings"
    server_ca_cert: SslCert
    ip_addresses: List[IpMapping]
    region: str
    database_version: Union[SqlDatabaseVersion, str]
    backend_type: Union[SqlBackendType, str]
    psc_enabled: Optional[bool]
    dns_name: Optional[str]

class SqlBackendType(Enum):
    ...

class SqlDatabaseVersion(Enum):
    # TODO: create this enum
    ...

class SslCert(JsonBase):
    kind: str = "sql#connectSettings"
    cert_serial_number: str
    cert: str
    create_time: datetime
    common_name: str
    expiration_time: datetime
    sha1_fingerprint: str
    instance: str
    self_link: Optional[str]

class IpMapping(JsonBase):
    sql_addr_type: SqlIpAddressType = Field(alias="type")
    ip_address: str
    time_to_retire: Optional[datetime]

class SqlIpAddressType(Enum):
    sql_ip_address_type_unspecified = "SQL_IP_ADDRESS_TYPE_UNSPECIFIED"
    primary = "PRIMARY"
    outgoing = "OUTGOING"
    private = "PRIVATE"
    migrated_1st_gen = "MIGRATED_1ST_GEN"

SqlConnection.update_forward_refs()
IpMapping.update_forward_refs()
