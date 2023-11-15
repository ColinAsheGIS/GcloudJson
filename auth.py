from google.cloud.iam_credentials import IAMCredentialsClient
import google.auth


async def get_creds():
    creds, project = google.auth.default()
    return creds, project


async def get_oauth_token():
    client = IAMCredentialsClient()
    service_account = 'colndev-405100@appspot.gserviceaccount.com'
    iam_sa_name = f'projects/-/serviceAccounts/{service_account}'
    request = client.generate_access_token(
        name=iam_sa_name,
        scope=['https://www.googleapis.com/auth/sqlservice.login']
    )
    return request.access_token
