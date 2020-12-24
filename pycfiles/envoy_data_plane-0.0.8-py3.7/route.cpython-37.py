# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/api/v2/route.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 71793 bytes
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List, Optional
import betterproto
from envoy_data_plane.envoy import type
from envoy_data_plane.envoy.api.v2 import core
from envoy_data_plane.envoy.type import matcher
from envoy_data_plane.envoy.type.tracing import v2
from envoy_data_plane.google import protobuf

class VirtualHostTlsRequirementType(betterproto.Enum):
    NONE = 0
    EXTERNAL_ONLY = 1
    ALL = 2


class RouteActionClusterNotFoundResponseCode(betterproto.Enum):
    SERVICE_UNAVAILABLE = 0
    NOT_FOUND = 1


class RouteActionInternalRedirectAction(betterproto.Enum):
    PASS_THROUGH_INTERNAL_REDIRECT = 0
    HANDLE_INTERNAL_REDIRECT = 1


class RedirectActionRedirectResponseCode(betterproto.Enum):
    MOVED_PERMANENTLY = 0
    FOUND = 1
    SEE_OTHER = 2
    TEMPORARY_REDIRECT = 3
    PERMANENT_REDIRECT = 4


@dataclass
class VirtualHost(betterproto.Message):
    __doc__ = "\n    The top level element in the routing configuration is a virtual host. Each\n    virtual host has a logical name as well as a set of domains that get routed\n    to it based on the incoming request's host header. This allows a single\n    listener to service multiple top level domain path trees. Once a virtual\n    host is selected based on the domain, the routes are processed in order to\n    see which upstream cluster to route to or whether to perform a redirect.\n    [#next-free-field: 19]\n    "
    name = betterproto.string_field(1)
    name: str
    domains = betterproto.string_field(2)
    domains: List[str]
    routes = betterproto.message_field(3)
    routes: List['Route']
    require_tls = betterproto.enum_field(4)
    require_tls: 'VirtualHostTlsRequirementType'
    virtual_clusters = betterproto.message_field(5)
    virtual_clusters: List['VirtualCluster']
    rate_limits = betterproto.message_field(6)
    rate_limits: List['RateLimit']
    request_headers_to_add = betterproto.message_field(7)
    request_headers_to_add: List[core.HeaderValueOption]
    request_headers_to_remove = betterproto.string_field(13)
    request_headers_to_remove: List[str]
    response_headers_to_add = betterproto.message_field(10)
    response_headers_to_add: List[core.HeaderValueOption]
    response_headers_to_remove = betterproto.string_field(11)
    response_headers_to_remove: List[str]
    cors = betterproto.message_field(8)
    cors: 'CorsPolicy'
    per_filter_config = betterproto.map_field(12, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    per_filter_config: Dict[(str, protobuf.Struct)]
    typed_per_filter_config = betterproto.map_field(15, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    typed_per_filter_config: Dict[(str, protobuf.Any)]
    include_request_attempt_count = betterproto.bool_field(14)
    include_request_attempt_count: bool
    retry_policy = betterproto.message_field(16)
    retry_policy: 'RetryPolicy'
    hedge_policy = betterproto.message_field(17)
    hedge_policy: 'HedgePolicy'
    per_request_buffer_limit_bytes = betterproto.message_field(18,
      wraps=(betterproto.TYPE_UINT32))
    per_request_buffer_limit_bytes: Optional[int]


@dataclass
class FilterAction(betterproto.Message):
    __doc__ = 'A filter-defined action type.'
    action = betterproto.message_field(1)
    action: protobuf.Any


@dataclass
class Route(betterproto.Message):
    __doc__ = '\n    A route is both a specification of how to match a request as well as an\n    indication of what to do next (e.g., redirect, forward, rewrite, etc.). ..\n    attention::   Envoy supports routing on HTTP method via :ref:`header\n    matching   <envoy_api_msg_route.HeaderMatcher>`. [#next-free-field: 18]\n    '
    name = betterproto.string_field(14)
    name: str
    match = betterproto.message_field(1)
    match: 'RouteMatch'
    route = betterproto.message_field(2, group='action')
    route: 'RouteAction'
    redirect = betterproto.message_field(3, group='action')
    redirect: 'RedirectAction'
    direct_response = betterproto.message_field(7,
      group='action')
    direct_response: 'DirectResponseAction'
    filter_action = betterproto.message_field(17, group='action')
    filter_action: 'FilterAction'
    metadata = betterproto.message_field(4)
    metadata: core.Metadata
    decorator = betterproto.message_field(5)
    decorator: 'Decorator'
    per_filter_config = betterproto.map_field(8, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    per_filter_config: Dict[(str, protobuf.Struct)]
    typed_per_filter_config = betterproto.map_field(13, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    typed_per_filter_config: Dict[(str, protobuf.Any)]
    request_headers_to_add = betterproto.message_field(9)
    request_headers_to_add: List[core.HeaderValueOption]
    request_headers_to_remove = betterproto.string_field(12)
    request_headers_to_remove: List[str]
    response_headers_to_add = betterproto.message_field(10)
    response_headers_to_add: List[core.HeaderValueOption]
    response_headers_to_remove = betterproto.string_field(11)
    response_headers_to_remove: List[str]
    tracing = betterproto.message_field(15)
    tracing: 'Tracing'
    per_request_buffer_limit_bytes = betterproto.message_field(16,
      wraps=(betterproto.TYPE_UINT32))
    per_request_buffer_limit_bytes: Optional[int]


@dataclass
class WeightedCluster(betterproto.Message):
    __doc__ = '\n    Compared to the :ref:`cluster <envoy_api_field_route.RouteAction.cluster>`\n    field that specifies a single upstream cluster as the target of a request,\n    the :ref:`weighted_clusters\n    <envoy_api_field_route.RouteAction.weighted_clusters>` option allows for\n    specification of multiple upstream clusters along with weights that\n    indicate the percentage of traffic to be forwarded to each cluster. The\n    router selects an upstream cluster based on the weights.\n    '
    clusters = betterproto.message_field(1)
    clusters: List['WeightedClusterClusterWeight']
    total_weight = betterproto.message_field(3,
      wraps=(betterproto.TYPE_UINT32))
    total_weight: Optional[int]
    runtime_key_prefix = betterproto.string_field(2)
    runtime_key_prefix: str


@dataclass
class WeightedClusterClusterWeight(betterproto.Message):
    __doc__ = '[#next-free-field: 11]'
    name = betterproto.string_field(1)
    name: str
    weight = betterproto.message_field(2, wraps=(betterproto.TYPE_UINT32))
    weight: Optional[int]
    metadata_match = betterproto.message_field(3)
    metadata_match: core.Metadata
    request_headers_to_add = betterproto.message_field(4)
    request_headers_to_add: List[core.HeaderValueOption]
    request_headers_to_remove = betterproto.string_field(9)
    request_headers_to_remove: List[str]
    response_headers_to_add = betterproto.message_field(5)
    response_headers_to_add: List[core.HeaderValueOption]
    response_headers_to_remove = betterproto.string_field(6)
    response_headers_to_remove: List[str]
    per_filter_config = betterproto.map_field(8, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    per_filter_config: Dict[(str, protobuf.Struct)]
    typed_per_filter_config = betterproto.map_field(10, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    typed_per_filter_config: Dict[(str, protobuf.Any)]


@dataclass
class RouteMatch(betterproto.Message):
    __doc__ = '[#next-free-field: 12]'
    prefix = betterproto.string_field(1, group='path_specifier')
    prefix: str
    path = betterproto.string_field(2, group='path_specifier')
    path: str
    regex = betterproto.string_field(3, group='path_specifier')
    regex: str
    safe_regex = betterproto.message_field(10,
      group='path_specifier')
    safe_regex: matcher.RegexMatcher
    case_sensitive = betterproto.message_field(4,
      wraps=(betterproto.TYPE_BOOL))
    case_sensitive: Optional[bool]
    runtime_fraction = betterproto.message_field(9)
    runtime_fraction: core.RuntimeFractionalPercent
    headers = betterproto.message_field(6)
    headers: List['HeaderMatcher']
    query_parameters = betterproto.message_field(7)
    query_parameters: List['QueryParameterMatcher']
    grpc = betterproto.message_field(8)
    grpc: 'RouteMatchGrpcRouteMatchOptions'
    tls_context = betterproto.message_field(11)
    tls_context: 'RouteMatchTlsContextMatchOptions'


@dataclass
class RouteMatchGrpcRouteMatchOptions(betterproto.Message):
    pass


@dataclass
class RouteMatchTlsContextMatchOptions(betterproto.Message):
    presented = betterproto.message_field(1,
      wraps=(betterproto.TYPE_BOOL))
    presented: Optional[bool]


@dataclass
class CorsPolicy(betterproto.Message):
    __doc__ = '[#next-free-field: 12]'
    allow_origin = betterproto.string_field(1)
    allow_origin: List[str]
    allow_origin_regex = betterproto.string_field(8)
    allow_origin_regex: List[str]
    allow_origin_string_match = betterproto.message_field(11)
    allow_origin_string_match: List[matcher.StringMatcher]
    allow_methods = betterproto.string_field(2)
    allow_methods: str
    allow_headers = betterproto.string_field(3)
    allow_headers: str
    expose_headers = betterproto.string_field(4)
    expose_headers: str
    max_age = betterproto.string_field(5)
    max_age: str
    allow_credentials = betterproto.message_field(6,
      wraps=(betterproto.TYPE_BOOL))
    allow_credentials: Optional[bool]
    enabled = betterproto.message_field(7,
      group='enabled_specifier', wraps=(betterproto.TYPE_BOOL))
    enabled: Optional[bool]
    filter_enabled = betterproto.message_field(9,
      group='enabled_specifier')
    filter_enabled: core.RuntimeFractionalPercent
    shadow_enabled = betterproto.message_field(10)
    shadow_enabled: core.RuntimeFractionalPercent


@dataclass
class RouteAction(betterproto.Message):
    __doc__ = '[#next-free-field: 32]'
    cluster = betterproto.string_field(1, group='cluster_specifier')
    cluster: str
    cluster_header = betterproto.string_field(2, group='cluster_specifier')
    cluster_header: str
    weighted_clusters = betterproto.message_field(3,
      group='cluster_specifier')
    weighted_clusters: 'WeightedCluster'
    cluster_not_found_response_code = betterproto.enum_field(20)
    cluster_not_found_response_code: 'RouteActionClusterNotFoundResponseCode'
    metadata_match = betterproto.message_field(4)
    metadata_match: core.Metadata
    prefix_rewrite = betterproto.string_field(5)
    prefix_rewrite: str
    host_rewrite = betterproto.string_field(6, group='host_rewrite_specifier')
    host_rewrite: str
    auto_host_rewrite = betterproto.message_field(7,
      group='host_rewrite_specifier', wraps=(betterproto.TYPE_BOOL))
    auto_host_rewrite: Optional[bool]
    auto_host_rewrite_header = betterproto.string_field(29,
      group='host_rewrite_specifier')
    auto_host_rewrite_header: str
    timeout = betterproto.message_field(8)
    timeout: timedelta
    idle_timeout = betterproto.message_field(24)
    idle_timeout: timedelta
    retry_policy = betterproto.message_field(9)
    retry_policy: 'RetryPolicy'
    request_mirror_policy = betterproto.message_field(10)
    request_mirror_policy: 'RouteActionRequestMirrorPolicy'
    request_mirror_policies = betterproto.message_field(30)
    request_mirror_policies: List['RouteActionRequestMirrorPolicy']
    priority = betterproto.enum_field(11)
    priority: core.RoutingPriority
    rate_limits = betterproto.message_field(13)
    rate_limits: List['RateLimit']
    include_vh_rate_limits = betterproto.message_field(14,
      wraps=(betterproto.TYPE_BOOL))
    include_vh_rate_limits: Optional[bool]
    hash_policy = betterproto.message_field(15)
    hash_policy: List['RouteActionHashPolicy']
    cors = betterproto.message_field(17)
    cors: 'CorsPolicy'
    max_grpc_timeout = betterproto.message_field(23)
    max_grpc_timeout: timedelta
    grpc_timeout_offset = betterproto.message_field(28)
    grpc_timeout_offset: timedelta
    upgrade_configs = betterproto.message_field(25)
    upgrade_configs: List['RouteActionUpgradeConfig']
    internal_redirect_action = betterproto.enum_field(26)
    internal_redirect_action: 'RouteActionInternalRedirectAction'
    max_internal_redirects = betterproto.message_field(31,
      wraps=(betterproto.TYPE_UINT32))
    max_internal_redirects: Optional[int]
    hedge_policy = betterproto.message_field(27)
    hedge_policy: 'HedgePolicy'


@dataclass
class RouteActionRequestMirrorPolicy(betterproto.Message):
    __doc__ = '\n    The router is capable of shadowing traffic from one cluster to another. The\n    current implementation is "fire and forget," meaning Envoy will not wait\n    for the shadow cluster to respond before returning the response from the\n    primary cluster. All normal statistics are collected for the shadow cluster\n    making this feature useful for testing. During shadowing, the\n    host/authority header is altered such that *-shadow* is appended. This is\n    useful for logging. For example, *cluster1* becomes *cluster1-shadow*. ..\n    note::   Shadowing will not be triggered if the primary cluster does not\n    exist.\n    '
    cluster = betterproto.string_field(1)
    cluster: str
    runtime_key = betterproto.string_field(2)
    runtime_key: str
    runtime_fraction = betterproto.message_field(3)
    runtime_fraction: core.RuntimeFractionalPercent


@dataclass
class RouteActionHashPolicy(betterproto.Message):
    __doc__ = "\n    Specifies the route's hashing policy if the upstream cluster uses a hashing\n    :ref:`load balancer <arch_overview_load_balancing_types>`. [#next-free-\n    field: 6]\n    "
    header = betterproto.message_field(1,
      group='policy_specifier')
    header: 'RouteActionHashPolicyHeader'
    cookie = betterproto.message_field(2,
      group='policy_specifier')
    cookie: 'RouteActionHashPolicyCookie'
    connection_properties = betterproto.message_field(3,
      group='policy_specifier')
    connection_properties: 'RouteActionHashPolicyConnectionProperties'
    query_parameter = betterproto.message_field(5,
      group='policy_specifier')
    query_parameter: 'RouteActionHashPolicyQueryParameter'
    terminal = betterproto.bool_field(4)
    terminal: bool


@dataclass
class RouteActionRouteActionHashPolicyHeader(betterproto.Message):
    header_name = betterproto.string_field(1)
    header_name: str


@dataclass
class RouteActionRouteActionHashPolicyCookie(betterproto.Message):
    __doc__ = "\n    Envoy supports two types of cookie affinity: 1. Passive. Envoy takes a\n    cookie that's present in the cookies header and    hashes on its value. 2.\n    Generated. Envoy generates and sets a cookie with an expiration (TTL)    on\n    the first request from the client in its response to the client,    based\n    on the endpoint the request gets sent to. The client then    presents this\n    on the next and all subsequent requests. The hash of    this is sufficient\n    to ensure these requests get sent to the same    endpoint. The cookie is\n    generated by hashing the source and    destination ports and addresses so\n    that multiple independent HTTP2    streams on the same connection will\n    independently receive the same    cookie, even if they arrive at the Envoy\n    simultaneously.\n    "
    name = betterproto.string_field(1)
    name: str
    ttl = betterproto.message_field(2)
    ttl: timedelta
    path = betterproto.string_field(3)
    path: str


@dataclass
class RouteActionRouteActionHashPolicyConnectionProperties(betterproto.Message):
    source_ip = betterproto.bool_field(1)
    source_ip: bool


@dataclass
class RouteActionRouteActionHashPolicyQueryParameter(betterproto.Message):
    name = betterproto.string_field(1)
    name: str


@dataclass
class RouteActionUpgradeConfig(betterproto.Message):
    __doc__ = '\n    Allows enabling and disabling upgrades on a per-route basis. This overrides\n    any enabled/disabled upgrade filter chain specified in the\n    HttpConnectionManager :ref:`upgrade_configs <envoy_api_field_config.filter.\n    network.http_connection_manager.v2.HttpConnectionManager.upgrade_configs>`\n    but does not affect any custom filter chain specified there.\n    '
    upgrade_type = betterproto.string_field(1)
    upgrade_type: str
    enabled = betterproto.message_field(2, wraps=(betterproto.TYPE_BOOL))
    enabled: Optional[bool]


@dataclass
class RetryPolicy(betterproto.Message):
    __doc__ = '\n    HTTP retry :ref:`architecture overview <arch_overview_http_routing_retry>`.\n    [#next-free-field: 11]\n    '
    retry_on = betterproto.string_field(1)
    retry_on: str
    num_retries = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    num_retries: Optional[int]
    per_try_timeout = betterproto.message_field(3)
    per_try_timeout: timedelta
    retry_priority = betterproto.message_field(4)
    retry_priority: 'RetryPolicyRetryPriority'
    retry_host_predicate = betterproto.message_field(5)
    retry_host_predicate: List['RetryPolicyRetryHostPredicate']
    host_selection_retry_max_attempts = betterproto.int64_field(6)
    host_selection_retry_max_attempts: int
    retriable_status_codes = betterproto.uint32_field(7)
    retriable_status_codes: List[int]
    retry_back_off = betterproto.message_field(8)
    retry_back_off: 'RetryPolicyRetryBackOff'
    retriable_headers = betterproto.message_field(9)
    retriable_headers: List['HeaderMatcher']
    retriable_request_headers = betterproto.message_field(10)
    retriable_request_headers: List['HeaderMatcher']


@dataclass
class RetryPolicyRetryPriority(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class RetryPolicyRetryHostPredicate(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class RetryPolicyRetryBackOff(betterproto.Message):
    base_interval = betterproto.message_field(1)
    base_interval: timedelta
    max_interval = betterproto.message_field(2)
    max_interval: timedelta


@dataclass
class HedgePolicy(betterproto.Message):
    __doc__ = '\n    HTTP request hedging :ref:`architecture overview\n    <arch_overview_http_routing_hedging>`.\n    '
    initial_requests = betterproto.message_field(1,
      wraps=(betterproto.TYPE_UINT32))
    initial_requests: Optional[int]
    additional_request_chance = betterproto.message_field(2)
    additional_request_chance: type.FractionalPercent
    hedge_on_per_try_timeout = betterproto.bool_field(3)
    hedge_on_per_try_timeout: bool


@dataclass
class RedirectAction(betterproto.Message):
    __doc__ = '[#next-free-field: 9]'
    https_redirect = betterproto.bool_field(4, group='scheme_rewrite_specifier')
    https_redirect: bool
    scheme_redirect = betterproto.string_field(7, group='scheme_rewrite_specifier')
    scheme_redirect: str
    host_redirect = betterproto.string_field(1)
    host_redirect: str
    port_redirect = betterproto.uint32_field(8)
    port_redirect: int
    path_redirect = betterproto.string_field(2, group='path_rewrite_specifier')
    path_redirect: str
    prefix_rewrite = betterproto.string_field(5, group='path_rewrite_specifier')
    prefix_rewrite: str
    response_code = betterproto.enum_field(3)
    response_code: 'RedirectActionRedirectResponseCode'
    strip_query = betterproto.bool_field(6)
    strip_query: bool


@dataclass
class DirectResponseAction(betterproto.Message):
    status = betterproto.uint32_field(1)
    status: int
    body = betterproto.message_field(2)
    body: core.DataSource


@dataclass
class Decorator(betterproto.Message):
    operation = betterproto.string_field(1)
    operation: str


@dataclass
class Tracing(betterproto.Message):
    client_sampling = betterproto.message_field(1)
    client_sampling: type.FractionalPercent
    random_sampling = betterproto.message_field(2)
    random_sampling: type.FractionalPercent
    overall_sampling = betterproto.message_field(3)
    overall_sampling: type.FractionalPercent
    custom_tags = betterproto.message_field(4)
    custom_tags: List[v2.CustomTag]


@dataclass
class VirtualCluster(betterproto.Message):
    __doc__ = '\n    A virtual cluster is a way of specifying a regex matching rule against\n    certain important endpoints such that statistics are generated explicitly\n    for the matched requests. The reason this is useful is that when doing\n    prefix/path matching Envoy does not always know what the application\n    considers to be an endpoint. Thus, it’s impossible for Envoy to generically\n    emit per endpoint statistics. However, often systems have highly critical\n    endpoints that they wish to get “perfect” statistics on. Virtual cluster\n    statistics are perfect in the sense that they are emitted on the downstream\n    side such that they include network level failures. Documentation for\n    :ref:`virtual cluster statistics <config_http_filters_router_stats>`. ..\n    note::    Virtual clusters are a useful tool, but we do not recommend\n    setting up a virtual cluster for    every application endpoint. This is\n    both not easily maintainable and as well the matching and    statistics\n    output are not free.\n    '
    pattern = betterproto.string_field(1)
    pattern: str
    headers = betterproto.message_field(4)
    headers: List['HeaderMatcher']
    name = betterproto.string_field(2)
    name: str
    method = betterproto.enum_field(3)
    method: core.RequestMethod


@dataclass
class RateLimit(betterproto.Message):
    __doc__ = '\n    Global rate limiting :ref:`architecture overview\n    <arch_overview_global_rate_limit>`.\n    '
    stage = betterproto.message_field(1, wraps=(betterproto.TYPE_UINT32))
    stage: Optional[int]
    disable_key = betterproto.string_field(2)
    disable_key: str
    actions = betterproto.message_field(3)
    actions: List['RateLimitAction']


@dataclass
class RateLimitAction(betterproto.Message):
    __doc__ = '[#next-free-field: 7]'
    source_cluster = betterproto.message_field(1,
      group='action_specifier')
    source_cluster: 'RateLimitActionSourceCluster'
    destination_cluster = betterproto.message_field(2,
      group='action_specifier')
    destination_cluster: 'RateLimitActionDestinationCluster'
    request_headers = betterproto.message_field(3,
      group='action_specifier')
    request_headers: 'RateLimitActionRequestHeaders'
    remote_address = betterproto.message_field(4,
      group='action_specifier')
    remote_address: 'RateLimitActionRemoteAddress'
    generic_key = betterproto.message_field(5,
      group='action_specifier')
    generic_key: 'RateLimitActionGenericKey'
    header_value_match = betterproto.message_field(6,
      group='action_specifier')
    header_value_match: 'RateLimitActionHeaderValueMatch'


@dataclass
class RateLimitRateLimitActionSourceCluster(betterproto.Message):
    __doc__ = '\n    The following descriptor entry is appended to the descriptor: .. code-\n    block:: cpp   ("source_cluster", "<local service cluster>") <local service\n    cluster> is derived from the :option:`--service-cluster` option.\n    '


@dataclass
class RateLimitRateLimitActionDestinationCluster(betterproto.Message):
    __doc__ = '\n    The following descriptor entry is appended to the descriptor: .. code-\n    block:: cpp   ("destination_cluster", "<routed target cluster>") Once a\n    request matches against a route table rule, a routed cluster is determined\n    by one of the following :ref:`route table configuration\n    <envoy_api_msg_RouteConfiguration>` settings: * :ref:`cluster\n    <envoy_api_field_route.RouteAction.cluster>` indicates the upstream cluster\n    to route to. * :ref:`weighted_clusters\n    <envoy_api_field_route.RouteAction.weighted_clusters>`   chooses a cluster\n    randomly from a set of clusters with attributed weight. *\n    :ref:`cluster_header <envoy_api_field_route.RouteAction.cluster_header>`\n    indicates which   header in the request contains the target cluster.\n    '


@dataclass
class RateLimitRateLimitActionRequestHeaders(betterproto.Message):
    __doc__ = '\n    The following descriptor entry is appended when a header contains a key\n    that matches the *header_name*: .. code-block:: cpp   ("<descriptor_key>",\n    "<header_value_queried_from_header>")\n    '
    header_name = betterproto.string_field(1)
    header_name: str
    descriptor_key = betterproto.string_field(2)
    descriptor_key: str


@dataclass
class RateLimitRateLimitActionRemoteAddress(betterproto.Message):
    __doc__ = '\n    The following descriptor entry is appended to the descriptor and is\n    populated using the trusted address from :ref:`x-forwarded-for\n    <config_http_conn_man_headers_x-forwarded-for>`: .. code-block:: cpp\n    ("remote_address", "<trusted address from x-forwarded-for>")\n    '


@dataclass
class RateLimitRateLimitActionGenericKey(betterproto.Message):
    __doc__ = '\n    The following descriptor entry is appended to the descriptor: .. code-\n    block:: cpp   ("generic_key", "<descriptor_value>")\n    '
    descriptor_value = betterproto.string_field(1)
    descriptor_value: str


@dataclass
class RateLimitRateLimitActionHeaderValueMatch(betterproto.Message):
    __doc__ = '\n    The following descriptor entry is appended to the descriptor: .. code-\n    block:: cpp   ("header_match", "<descriptor_value>")\n    '
    descriptor_value = betterproto.string_field(1)
    descriptor_value: str
    expect_match = betterproto.message_field(2,
      wraps=(betterproto.TYPE_BOOL))
    expect_match: Optional[bool]
    headers = betterproto.message_field(3)
    headers: List['HeaderMatcher']


@dataclass
class HeaderMatcher(betterproto.Message):
    __doc__ = '\n    .. attention::   Internally, Envoy always uses the HTTP/2 *:authority*\n    header to represent the HTTP/1 *Host*   header. Thus, if attempting to\n    match on *Host*, match on *:authority* instead. .. attention::   To route\n    on HTTP method, use the special HTTP/2 *:method* header. This works for\n    both   HTTP/1 and HTTP/2 as Envoy normalizes headers. E.g.,   .. code-\n    block:: json     {       "name": ":method",       "exact_match": "POST"\n    } .. attention::   In the absence of any header match specifier, match will\n    default to :ref:`present_match\n    <envoy_api_field_route.HeaderMatcher.present_match>`. i.e, a request that\n    has the :ref:`name   <envoy_api_field_route.HeaderMatcher.name>` header\n    will match, regardless of the header\'s   value.  [#next-major-version:\n    HeaderMatcher should be refactored to use StringMatcher.] [#next-free-\n    field: 12]\n    '
    name = betterproto.string_field(1)
    name: str
    exact_match = betterproto.string_field(4, group='header_match_specifier')
    exact_match: str
    regex_match = betterproto.string_field(5, group='header_match_specifier')
    regex_match: str
    safe_regex_match = betterproto.message_field(11,
      group='header_match_specifier')
    safe_regex_match: matcher.RegexMatcher
    range_match = betterproto.message_field(6,
      group='header_match_specifier')
    range_match: type.Int64Range
    present_match = betterproto.bool_field(7, group='header_match_specifier')
    present_match: bool
    prefix_match = betterproto.string_field(9, group='header_match_specifier')
    prefix_match: str
    suffix_match = betterproto.string_field(10, group='header_match_specifier')
    suffix_match: str
    invert_match = betterproto.bool_field(8)
    invert_match: bool


@dataclass
class QueryParameterMatcher(betterproto.Message):
    __doc__ = "\n    Query parameter matching treats the query string of a request's :path\n    header as an ampersand-separated list of keys and/or key=value elements.\n    [#next-free-field: 7]\n    "
    name = betterproto.string_field(1)
    name: str
    value = betterproto.string_field(3)
    value: str
    regex = betterproto.message_field(4, wraps=(betterproto.TYPE_BOOL))
    regex: Optional[bool]
    string_match = betterproto.message_field(5,
      group='query_parameter_match_specifier')
    string_match: matcher.StringMatcher
    present_match = betterproto.bool_field(6,
      group='query_parameter_match_specifier')
    present_match: bool