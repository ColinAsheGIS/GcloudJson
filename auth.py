from __future__ import annotations

from google.cloud.iam_credentials import IAMCredentialsClient
import google.auth


async def get_creds():
    creds, project = google.auth.default()
    return creds, project


def get_oauth_token(scope: str):
    client = IAMCredentialsClient()
    service_account = 'colndev-405100@appspot.gserviceaccount.com'
    iam_sa_name = f'projects/-/serviceAccounts/{service_account}'
    request = client.generate_access_token(
        name=iam_sa_name,
        scope=[scope]
    )
    return request.access_token


async def async_get_oauth_token():
    client = IAMCredentialsClient()
    service_account = 'colndev-405100@appspot.gserviceaccount.com'
    iam_sa_name = f'projects/-/serviceAccounts/{service_account}'
    request = client.generate_access_token(
        name=iam_sa_name,
        scope=['https://www.googleapis.com/auth/sqlservice.login']
    )
    return request.access_token


def get_sql_oauth_token():
    client = IAMCredentialsClient()
    service_account = 'colndev-405100@appspot.gserviceaccount.com'
    iam_sa_name = f'projects/-/serviceAccounts/{service_account}'
    request = client.generate_access_token(
        name=iam_sa_name,
        scope=['https://www.googleapis.com/auth/sqlservice.admin']
    )
    return request.access_token


def get_drive_oauth_token():
    client = IAMCredentialsClient()
    service_account = 'colndev-405100@appspot.gserviceaccount.com'
    iam_sa_name = f'projects/-/serviceAccounts/{service_account}'
    request = client.generate_access_token(
        name=iam_sa_name,
        scope=['https://www.googleapis.com/auth/drive']
    )
    return request.access_token


def get_pubsub_oath_token():
    return get_oauth_token("https://www.googleapis.com/auth/pubsub")


def get_scheduler_oauth_token():
    return get_oauth_token("https://www.googleapis.com/auth/cloud-scheduler")
