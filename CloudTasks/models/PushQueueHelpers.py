from kaffeine import get_project_settings

from base_types import JsonHTTPMethod

from .PushQueue import JsonAppEngineHttpQueue , JsonHTTPTarget, JsonPathOverride, JsonPushQueueInput, \
    JsonQueryOverride, JsonRateLimits, JsonRetryConfig, JsonUriOverride, OidcToken, Scheme, StackdriverLoggingConfig, \
    UriOverrideEnforceMode, JsonAppEngineRouting


def create_push_queue_url(basepath: str, project_id: str, location_id: str) -> str:
    return f"{basepath}/projects/{project_id}/locations/{location_id}/queues"


def create_default_uri_override() -> JsonUriOverride:
    path_override = JsonPathOverride(path="")
    query_override = JsonQueryOverride(query_params="")
    uri_override = UriOverrideEnforceMode.uri_override_enforce_mode_unspecified
    scheme = Scheme.scheme_unspecified
    host = None
    port = None
    res = JsonUriOverride(
        path_override=path_override,
        query_override=query_override,
        uri_override_enforce_mode=uri_override,
        scheme=scheme,
        host=host,
        port=port
    )
    return res


async def create_default_oidc_token() -> OidcToken:
    settings = get_project_settings(base_settings=True)
    return OidcToken(
        service_account_email=f'{settings.current_service}@appspot.gserviceaccount.com',
        audience="https://www.googleapis.com/auth/cloud-tasks"
    )


async def create_default_http_target() -> JsonHTTPTarget:
    uri_override = create_default_uri_override()
    http_method = JsonHTTPMethod.post
    header_overrides = []
    oidc_token = await create_default_oidc_token()
    json_http_target = JsonHTTPTarget(
        uri_override=uri_override,
        http_method=http_method,
        header_overrides=header_overrides,
        oidc_token=oidc_token
    )
    return json_http_target


async def create_default_push_queue_request(queue_name: str) -> JsonPushQueueInput:
    name = f"projects/kapi-development/locations/us-central1/queues/{queue_name}"
    http_target = await create_default_http_target()
    rate_limits = JsonRateLimits()
    retry_config = JsonRetryConfig()
    stackdriver_logging_config = StackdriverLoggingConfig()
    app_engine_http_queue = JsonAppEngineHttpQueue(app_engine_routing_override=JsonAppEngineRouting())
    res = JsonPushQueueInput(
        name=name,
        http_target=http_target,
        rate_limits=rate_limits,
        retry_config=retry_config,
        stackdriver_logging_config=stackdriver_logging_config,
        app_engine_http_queue=app_engine_http_queue
    )
    return res
