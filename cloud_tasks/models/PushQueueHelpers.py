from .PushQueue import JsonAppEngineHttpQueue, JsonHTTPMethod, JsonHTTPTarget, JsonPathOverride, JsonPushQueueInput, JsonQueryOverride, JsonRateLimits, JsonRetryConfig, JsonUriOverride, OidcToken, Scheme, StackdriverLoggingConfig, State, UriOverrideEnforceMode

def create_push_queue_url(basepath: str, project_id: str, location_id: str) -> str:
    return f"{basepath}/projects/{project_id}/locations/{location_id}/queues"

def create_default_uri_override() -> JsonUriOverride:
    path_override = JsonPathOverride(path="")
    query_override = JsonQueryOverride(query_params="")
    uri_override = UriOverrideEnforceMode.uri_override_enforce_mode_unspecified
    scheme = Scheme.scheme_unspecified
    host = ""
    port = ""
    res = JsonUriOverride(
        path_override=path_override,
        query_override=query_override,
        uri_override_enforce_mode=uri_override,
        scheme=scheme,
        host=host,
        port=port
    )
    return res

def create_default_oidc_token() -> OidcToken:
    service_account_email = "colin@getkoffie.com"
    scope = "a scope"
    return OidcToken(
        service_account_email=service_account_email,
        scope=scope
    )

def create_default_http_target() -> JsonHTTPTarget:
    uri_override = create_default_uri_override()
    http_method = JsonHTTPMethod.post
    header_overrides = []
    oidc_token = create_default_oidc_token()
    json_http_target = JsonHTTPTarget(
        uri_override=uri_override,
        http_method=http_method,
        header_overrides=header_overrides,
        oidc_token=oidc_token
    )
    return json_http_target

def create_default_push_queue_request() -> JsonPushQueueInput:
    name = "test_queue_1"
    http_target = create_default_http_target()
    rate_limits = JsonRateLimits()
    retry_config = JsonRetryConfig()
    stackdriver_logging_config = StackdriverLoggingConfig()
    res = JsonPushQueueInput(
        name=name,
        http_target=http_target,
        rate_limits=rate_limits,
        retry_config=retry_config,
        stackdriver_logging_config=stackdriver_logging_config
    )
    return res
