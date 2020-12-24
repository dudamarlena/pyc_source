# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/api/v2/core.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 63018 bytes
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List, Optional
import betterproto
from envoy_data_plane.envoy import type
from envoy_data_plane.envoy.type import matcher
from envoy_data_plane.google import protobuf

class RoutingPriority(betterproto.Enum):
    __doc__ = '\n    Envoy supports :ref:`upstream priority routing\n    <arch_overview_http_routing_priority>` both at the route and the virtual\n    cluster level. The current priority implementation uses different\n    connection pool and circuit breaking settings for each priority level. This\n    means that even for HTTP/2 requests, two physical connections will be used\n    to an upstream host. In the future Envoy will likely support true HTTP/2\n    priority over a single upstream connection.\n    '
    DEFAULT = 0
    HIGH = 1


class RequestMethod(betterproto.Enum):
    __doc__ = 'HTTP request method.'
    METHOD_UNSPECIFIED = 0
    GET = 1
    HEAD = 2
    POST = 3
    PUT = 4
    DELETE = 5
    CONNECT = 6
    OPTIONS = 7
    TRACE = 8
    PATCH = 9


class TrafficDirection(betterproto.Enum):
    __doc__ = 'Identifies the direction of the traffic relative to the local Envoy.'
    UNSPECIFIED = 0
    INBOUND = 1
    OUTBOUND = 2


class SocketOptionSocketState(betterproto.Enum):
    STATE_PREBIND = 0
    STATE_BOUND = 1
    STATE_LISTENING = 2


class ApiVersion(betterproto.Enum):
    __doc__ = '\n    xDS API version. This is used to describe both resource and transport\n    protocol versions (in distinct configuration fields).\n    '
    AUTO = 0
    V2 = 1
    V3 = 2


class ApiConfigSourceApiType(betterproto.Enum):
    UNSUPPORTED_REST_LEGACY = 0
    REST = 1
    GRPC = 2
    DELTA_GRPC = 3


class SocketAddressProtocol(betterproto.Enum):
    TCP = 0
    UDP = 1


class HealthStatus(betterproto.Enum):
    __doc__ = 'Endpoint health status.'
    UNKNOWN = 0
    HEALTHY = 1
    UNHEALTHY = 2
    DRAINING = 3
    TIMEOUT = 4
    DEGRADED = 5


@dataclass
class HttpUri(betterproto.Message):
    __doc__ = 'Envoy external URI descriptor'
    uri = betterproto.string_field(1)
    uri: str
    cluster = betterproto.string_field(2, group='http_upstream_type')
    cluster: str
    timeout = betterproto.message_field(3)
    timeout: timedelta


@dataclass
class Locality(betterproto.Message):
    __doc__ = '\n    Identifies location of where either Envoy runs or where upstream hosts run.\n    '
    region = betterproto.string_field(1)
    region: str
    zone = betterproto.string_field(2)
    zone: str
    sub_zone = betterproto.string_field(3)
    sub_zone: str


@dataclass
class BuildVersion(betterproto.Message):
    __doc__ = "\n    BuildVersion combines SemVer version of extension with free-form build\n    information (i.e. 'alpha', 'private-build') as a set of strings.\n    "
    version = betterproto.message_field(1)
    version: type.SemanticVersion
    metadata = betterproto.message_field(2)
    metadata: protobuf.Struct


@dataclass
class Extension(betterproto.Message):
    __doc__ = '\n    Version and identification for an Envoy extension. [#next-free-field: 6]\n    '
    name = betterproto.string_field(1)
    name: str
    category = betterproto.string_field(2)
    category: str
    type_descriptor = betterproto.string_field(3)
    type_descriptor: str
    version = betterproto.message_field(4)
    version: 'BuildVersion'
    disabled = betterproto.bool_field(5)
    disabled: bool


@dataclass
class Node(betterproto.Message):
    __doc__ = '\n    Identifies a specific Envoy instance. The node identifier is presented to\n    the management server, which may use this identifier to distinguish per\n    Envoy configuration for serving. [#next-free-field: 11]\n    '
    id = betterproto.string_field(1)
    id: str
    cluster = betterproto.string_field(2)
    cluster: str
    metadata = betterproto.message_field(3)
    metadata: protobuf.Struct
    locality = betterproto.message_field(4)
    locality: 'Locality'
    build_version = betterproto.string_field(5)
    build_version: str
    user_agent_name = betterproto.string_field(6)
    user_agent_name: str
    user_agent_version = betterproto.string_field(7,
      group='user_agent_version_type')
    user_agent_version: str
    user_agent_build_version = betterproto.message_field(8,
      group='user_agent_version_type')
    user_agent_build_version: 'BuildVersion'
    extensions = betterproto.message_field(9)
    extensions: List['Extension']
    client_features = betterproto.string_field(10)
    client_features: List[str]


@dataclass
class Metadata(betterproto.Message):
    __doc__ = '\n    Metadata provides additional inputs to filters based on matched listeners,\n    filter chains, routes and endpoints. It is structured as a map, usually\n    from filter name (in reverse DNS format) to metadata specific to the\n    filter. Metadata key-values for a filter are merged as connection and\n    request handling occurs, with later values for the same key overriding\n    earlier values. An example use of metadata is providing additional values\n    to http_connection_manager in the envoy.http_connection_manager.access_log\n    namespace. Another example use of metadata is to per service config info in\n    cluster metadata, which may get consumed by multiple filters. For load\n    balancing, Metadata provides a means to subset cluster endpoints. Endpoints\n    have a Metadata object associated and routes contain a Metadata object to\n    match against. There are some well defined metadata used today for this\n    purpose: * ``{"envoy.lb": {"canary": <bool> }}`` This indicates the canary\n    status of an   endpoint and is also used during header processing\n    (x-envoy-upstream-canary) and for stats purposes. [#next-major-version:\n    move to type/metadata/v2]\n    '
    filter_metadata = betterproto.map_field(1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    filter_metadata: Dict[(str, protobuf.Struct)]


@dataclass
class RuntimeUInt32(betterproto.Message):
    __doc__ = 'Runtime derived uint32 with a default when not specified.'
    default_value = betterproto.uint32_field(2)
    default_value: int
    runtime_key = betterproto.string_field(3)
    runtime_key: str


@dataclass
class RuntimeFeatureFlag(betterproto.Message):
    __doc__ = 'Runtime derived bool with a default when not specified.'
    default_value = betterproto.message_field(1,
      wraps=(betterproto.TYPE_BOOL))
    default_value: Optional[bool]
    runtime_key = betterproto.string_field(2)
    runtime_key: str


@dataclass
class HeaderValue(betterproto.Message):
    __doc__ = 'Header name/value pair.'
    key = betterproto.string_field(1)
    key: str
    value = betterproto.string_field(2)
    value: str


@dataclass
class HeaderValueOption(betterproto.Message):
    __doc__ = 'Header name/value pair plus option to control append behavior.'
    header = betterproto.message_field(1)
    header: 'HeaderValue'
    append = betterproto.message_field(2, wraps=(betterproto.TYPE_BOOL))
    append: Optional[bool]


@dataclass
class HeaderMap(betterproto.Message):
    __doc__ = 'Wrapper for a set of headers.'
    headers = betterproto.message_field(1)
    headers: List['HeaderValue']


@dataclass
class DataSource(betterproto.Message):
    __doc__ = 'Data source consisting of either a file or an inline value.'
    filename = betterproto.string_field(1, group='specifier')
    filename: str
    inline_bytes = betterproto.bytes_field(2, group='specifier')
    inline_bytes: bytes
    inline_string = betterproto.string_field(3, group='specifier')
    inline_string: str


@dataclass
class RemoteDataSource(betterproto.Message):
    __doc__ = '\n    The message specifies how to fetch data from remote and how to verify it.\n    '
    http_uri = betterproto.message_field(1)
    http_uri: 'HttpUri'
    sha256 = betterproto.string_field(2)
    sha256: str


@dataclass
class AsyncDataSource(betterproto.Message):
    __doc__ = 'Async data source which support async data fetch.'
    local = betterproto.message_field(1, group='specifier')
    local: 'DataSource'
    remote = betterproto.message_field(2, group='specifier')
    remote: 'RemoteDataSource'


@dataclass
class TransportSocket(betterproto.Message):
    __doc__ = '\n    Configuration for transport socket in :ref:`listeners <config_listeners>`\n    and :ref:`clusters <envoy_api_msg_Cluster>`. If the configuration is empty,\n    a default transport socket implementation and configuration will be chosen\n    based on the platform and existence of tls_context.\n    '
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class SocketOption(betterproto.Message):
    __doc__ = '\n    Generic socket option message. This would be used to set socket options\n    that might not exist in upstream kernels or precompiled Envoy binaries.\n    [#next-free-field: 7]\n    '
    description = betterproto.string_field(1)
    description: str
    level = betterproto.int64_field(2)
    level: int
    name = betterproto.int64_field(3)
    name: int
    int_value = betterproto.int64_field(4, group='value')
    int_value: int
    buf_value = betterproto.bytes_field(5, group='value')
    buf_value: bytes
    state = betterproto.enum_field(6)
    state: 'SocketOptionSocketState'


@dataclass
class RuntimeFractionalPercent(betterproto.Message):
    __doc__ = '\n    Runtime derived FractionalPercent with defaults for when the numerator or\n    denominator is not specified via a runtime key. .. note::   Parsing of the\n    runtime key\'s data is implemented such that it may be represented as a\n    :ref:`FractionalPercent <envoy_api_msg_type.FractionalPercent>` proto\n    represented as JSON/YAML   and may also be represented as an integer with\n    the assumption that the value is an integral   percentage out of 100. For\n    instance, a runtime key lookup returning the value "42" would parse   as a\n    `FractionalPercent` whose numerator is 42 and denominator is HUNDRED.\n    '
    default_value = betterproto.message_field(1)
    default_value: type.FractionalPercent
    runtime_key = betterproto.string_field(2)
    runtime_key: str


@dataclass
class ControlPlane(betterproto.Message):
    __doc__ = '\n    Identifies a specific ControlPlane instance that Envoy is connected to.\n    '
    identifier = betterproto.string_field(1)
    identifier: str


@dataclass
class GrpcService(betterproto.Message):
    __doc__ = '\n    gRPC service configuration. This is used by :ref:`ApiConfigSource\n    <envoy_api_msg_core.ApiConfigSource>` and filter configurations. [#next-\n    free-field: 6]\n    '
    envoy_grpc = betterproto.message_field(1,
      group='target_specifier')
    envoy_grpc: 'GrpcServiceEnvoyGrpc'
    google_grpc = betterproto.message_field(2,
      group='target_specifier')
    google_grpc: 'GrpcServiceGoogleGrpc'
    timeout = betterproto.message_field(3)
    timeout: timedelta
    initial_metadata = betterproto.message_field(5)
    initial_metadata: List['HeaderValue']


@dataclass
class GrpcServiceEnvoyGrpc(betterproto.Message):
    cluster_name = betterproto.string_field(1)
    cluster_name: str


@dataclass
class GrpcServiceGoogleGrpc(betterproto.Message):
    __doc__ = '[#next-free-field: 7]'
    target_uri = betterproto.string_field(1)
    target_uri: str
    channel_credentials = betterproto.message_field(2)
    channel_credentials: 'GrpcServiceGoogleGrpcChannelCredentials'
    call_credentials = betterproto.message_field(3)
    call_credentials: List['GrpcServiceGoogleGrpcCallCredentials']
    stat_prefix = betterproto.string_field(4)
    stat_prefix: str
    credentials_factory_name = betterproto.string_field(5)
    credentials_factory_name: str
    config = betterproto.message_field(6)
    config: protobuf.Struct


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcSslCredentials(betterproto.Message):
    __doc__ = '\n    See https://grpc.io/grpc/cpp/structgrpc_1_1_ssl_credentials_options.html.\n    '
    root_certs = betterproto.message_field(1)
    root_certs: 'DataSource'
    private_key = betterproto.message_field(2)
    private_key: 'DataSource'
    cert_chain = betterproto.message_field(3)
    cert_chain: 'DataSource'


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcGoogleLocalCredentials(betterproto.Message):
    __doc__ = '\n    Local channel credentials. Only UDS is supported for now. See\n    https://github.com/grpc/grpc/pull/15909.\n    '


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcChannelCredentials(betterproto.Message):
    __doc__ = '\n    See https://grpc.io/docs/guides/auth.html#credential-types to understand\n    Channel and Call credential types.\n    '
    ssl_credentials = betterproto.message_field(1,
      group='credential_specifier')
    ssl_credentials: 'GrpcServiceGoogleGrpcSslCredentials'
    google_default = betterproto.message_field(2,
      group='credential_specifier')
    google_default: protobuf.Empty
    local_credentials = betterproto.message_field(3,
      group='credential_specifier')
    local_credentials: 'GrpcServiceGoogleGrpcGoogleLocalCredentials'


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcCallCredentials(betterproto.Message):
    __doc__ = '[#next-free-field: 8]'
    access_token = betterproto.string_field(1, group='credential_specifier')
    access_token: str
    google_compute_engine = betterproto.message_field(2,
      group='credential_specifier')
    google_compute_engine: protobuf.Empty
    google_refresh_token = betterproto.string_field(3,
      group='credential_specifier')
    google_refresh_token: str
    service_account_jwt_access = betterproto.message_field(4,
      group='credential_specifier')
    service_account_jwt_access: 'GrpcServiceGoogleGrpcCallCredentialsServiceAccountJWTAccessCredentials'
    google_iam = betterproto.message_field(5,
      group='credential_specifier')
    google_iam: 'GrpcServiceGoogleGrpcCallCredentialsGoogleIAMCredentials'
    from_plugin = betterproto.message_field(6,
      group='credential_specifier')
    from_plugin: 'GrpcServiceGoogleGrpcCallCredentialsMetadataCredentialsFromPlugin'
    sts_service = betterproto.message_field(7,
      group='credential_specifier')
    sts_service: 'GrpcServiceGoogleGrpcCallCredentialsStsService'


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcGrpcServiceGrpcServiceGoogleGrpcCallCredentialsServiceAccountJWTAccessCredentials(betterproto.Message):
    json_key = betterproto.string_field(1)
    json_key: str
    token_lifetime_seconds = betterproto.uint64_field(2)
    token_lifetime_seconds: int


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcGrpcServiceGrpcServiceGoogleGrpcCallCredentialsGoogleIAMCredentials(betterproto.Message):
    authorization_token = betterproto.string_field(1)
    authorization_token: str
    authority_selector = betterproto.string_field(2)
    authority_selector: str


@dataclass
class GrpcServiceGrpcServiceGoogleGrpcGrpcServiceGrpcServiceGoogleGrpcCallCredentialsMetadataCredentialsFromPlugin(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class GrpcServiceGoogleGrpcCallCredentialsStsService(betterproto.Message):
    __doc__ = '\n    Security token service configuration that allows Google gRPC to fetch\n    security token from an OAuth 2.0 authorization server. See\n    https://tools.ietf.org/html/draft-ietf-oauth-token-exchange-16 and\n    https://github.com/grpc/grpc/pull/19587. [#next-free-field: 10]\n    '
    token_exchange_service_uri = betterproto.string_field(1)
    token_exchange_service_uri: str
    resource = betterproto.string_field(2)
    resource: str
    audience = betterproto.string_field(3)
    audience: str
    scope = betterproto.string_field(4)
    scope: str
    requested_token_type = betterproto.string_field(5)
    requested_token_type: str
    subject_token_path = betterproto.string_field(6)
    subject_token_path: str
    subject_token_type = betterproto.string_field(7)
    subject_token_type: str
    actor_token_path = betterproto.string_field(8)
    actor_token_path: str
    actor_token_type = betterproto.string_field(9)
    actor_token_type: str


@dataclass
class ApiConfigSource(betterproto.Message):
    __doc__ = '\n    API configuration source. This identifies the API type and cluster that\n    Envoy will use to fetch an xDS API. [#next-free-field: 9]\n    '
    api_type = betterproto.enum_field(1)
    api_type: 'ApiConfigSourceApiType'
    transport_api_version = betterproto.enum_field(8)
    transport_api_version: 'ApiVersion'
    cluster_names = betterproto.string_field(2)
    cluster_names: List[str]
    grpc_services = betterproto.message_field(4)
    grpc_services: List['GrpcService']
    refresh_delay = betterproto.message_field(3)
    refresh_delay: timedelta
    request_timeout = betterproto.message_field(5)
    request_timeout: timedelta
    rate_limit_settings = betterproto.message_field(6)
    rate_limit_settings: 'RateLimitSettings'
    set_node_on_first_message_only = betterproto.bool_field(7)
    set_node_on_first_message_only: bool


@dataclass
class AggregatedConfigSource(betterproto.Message):
    __doc__ = '\n    Aggregated Discovery Service (ADS) options. This is currently empty, but\n    when set in :ref:`ConfigSource <envoy_api_msg_core.ConfigSource>` can be\n    used to specify that ADS is to be used.\n    '


@dataclass
class SelfConfigSource(betterproto.Message):
    __doc__ = '\n    [#not-implemented-hide:] Self-referencing config source options. This is\n    currently empty, but when set in :ref:`ConfigSource\n    <envoy_api_msg_core.ConfigSource>` can be used to specify that other data\n    can be obtained from the same server.\n    '


@dataclass
class RateLimitSettings(betterproto.Message):
    __doc__ = '\n    Rate Limit settings to be applied for discovery requests made by Envoy.\n    '
    max_tokens = betterproto.message_field(1,
      wraps=(betterproto.TYPE_UINT32))
    max_tokens: Optional[int]
    fill_rate = betterproto.message_field(2,
      wraps=(betterproto.TYPE_DOUBLE))
    fill_rate: Optional[float]


@dataclass
class ConfigSource(betterproto.Message):
    __doc__ = '\n    Configuration for :ref:`listeners <config_listeners>`, :ref:`clusters\n    <config_cluster_manager>`, :ref:`routes\n    <envoy_api_msg_RouteConfiguration>`, :ref:`endpoints\n    <arch_overview_service_discovery>` etc. may either be sourced from the\n    filesystem or from an xDS API source. Filesystem configs are watched with\n    inotify for updates. [#next-free-field: 7]\n    '
    path = betterproto.string_field(1, group='config_source_specifier')
    path: str
    api_config_source = betterproto.message_field(2,
      group='config_source_specifier')
    api_config_source: 'ApiConfigSource'
    ads = betterproto.message_field(3,
      group='config_source_specifier')
    ads: 'AggregatedConfigSource'
    self = betterproto.message_field(5,
      group='config_source_specifier')
    self: 'SelfConfigSource'
    initial_fetch_timeout = betterproto.message_field(4)
    initial_fetch_timeout: timedelta
    resource_api_version = betterproto.enum_field(6)
    resource_api_version: 'ApiVersion'


@dataclass
class Pipe(betterproto.Message):
    path = betterproto.string_field(1)
    path: str
    mode = betterproto.uint32_field(2)
    mode: int


@dataclass
class SocketAddress(betterproto.Message):
    __doc__ = '[#next-free-field: 7]'
    protocol = betterproto.enum_field(1)
    protocol: 'SocketAddressProtocol'
    address = betterproto.string_field(2)
    address: str
    port_value = betterproto.uint32_field(3, group='port_specifier')
    port_value: int
    named_port = betterproto.string_field(4, group='port_specifier')
    named_port: str
    resolver_name = betterproto.string_field(5)
    resolver_name: str
    ipv4_compat = betterproto.bool_field(6)
    ipv4_compat: bool


@dataclass
class TcpKeepalive(betterproto.Message):
    keepalive_probes = betterproto.message_field(1,
      wraps=(betterproto.TYPE_UINT32))
    keepalive_probes: Optional[int]
    keepalive_time = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    keepalive_time: Optional[int]
    keepalive_interval = betterproto.message_field(3,
      wraps=(betterproto.TYPE_UINT32))
    keepalive_interval: Optional[int]


@dataclass
class BindConfig(betterproto.Message):
    source_address = betterproto.message_field(1)
    source_address: 'SocketAddress'
    freebind = betterproto.message_field(2, wraps=(betterproto.TYPE_BOOL))
    freebind: Optional[bool]
    socket_options = betterproto.message_field(3)
    socket_options: List['SocketOption']


@dataclass
class Address(betterproto.Message):
    __doc__ = '\n    Addresses specify either a logical or physical address and port, which are\n    used to tell Envoy where to bind/listen, connect to upstream and find\n    management servers.\n    '
    socket_address = betterproto.message_field(1, group='address')
    socket_address: 'SocketAddress'
    pipe = betterproto.message_field(2, group='address')
    pipe: 'Pipe'


@dataclass
class CidrRange(betterproto.Message):
    __doc__ = '\n    CidrRange specifies an IP Address and a prefix length to construct the\n    subnet mask for a `CIDR <https://tools.ietf.org/html/rfc4632>`_ range.\n    '
    address_prefix = betterproto.string_field(1)
    address_prefix: str
    prefix_len = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    prefix_len: Optional[int]


@dataclass
class HealthCheck(betterproto.Message):
    __doc__ = '[#next-free-field: 22]'
    timeout = betterproto.message_field(1)
    timeout: timedelta
    interval = betterproto.message_field(2)
    interval: timedelta
    initial_jitter = betterproto.message_field(20)
    initial_jitter: timedelta
    interval_jitter = betterproto.message_field(3)
    interval_jitter: timedelta
    interval_jitter_percent = betterproto.uint32_field(18)
    interval_jitter_percent: int
    unhealthy_threshold = betterproto.message_field(4,
      wraps=(betterproto.TYPE_UINT32))
    unhealthy_threshold: Optional[int]
    healthy_threshold = betterproto.message_field(5,
      wraps=(betterproto.TYPE_UINT32))
    healthy_threshold: Optional[int]
    alt_port = betterproto.message_field(6,
      wraps=(betterproto.TYPE_UINT32))
    alt_port: Optional[int]
    reuse_connection = betterproto.message_field(7,
      wraps=(betterproto.TYPE_BOOL))
    reuse_connection: Optional[bool]
    http_health_check = betterproto.message_field(8,
      group='health_checker')
    http_health_check: 'HealthCheckHttpHealthCheck'
    tcp_health_check = betterproto.message_field(9,
      group='health_checker')
    tcp_health_check: 'HealthCheckTcpHealthCheck'
    grpc_health_check = betterproto.message_field(11,
      group='health_checker')
    grpc_health_check: 'HealthCheckGrpcHealthCheck'
    custom_health_check = betterproto.message_field(13,
      group='health_checker')
    custom_health_check: 'HealthCheckCustomHealthCheck'
    no_traffic_interval = betterproto.message_field(12)
    no_traffic_interval: timedelta
    unhealthy_interval = betterproto.message_field(14)
    unhealthy_interval: timedelta
    unhealthy_edge_interval = betterproto.message_field(15)
    unhealthy_edge_interval: timedelta
    healthy_edge_interval = betterproto.message_field(16)
    healthy_edge_interval: timedelta
    event_log_path = betterproto.string_field(17)
    event_log_path: str
    always_log_health_check_failures = betterproto.bool_field(19)
    always_log_health_check_failures: bool
    tls_options = betterproto.message_field(21)
    tls_options: 'HealthCheckTlsOptions'


@dataclass
class HealthCheckPayload(betterproto.Message):
    __doc__ = 'Describes the encoding of the payload bytes in the payload.'
    text = betterproto.string_field(1, group='payload')
    text: str
    binary = betterproto.bytes_field(2, group='payload')
    binary: bytes


@dataclass
class HealthCheckHttpHealthCheck(betterproto.Message):
    __doc__ = '[#next-free-field: 12]'
    host = betterproto.string_field(1)
    host: str
    path = betterproto.string_field(2)
    path: str
    send = betterproto.message_field(3)
    send: 'HealthCheckPayload'
    receive = betterproto.message_field(4)
    receive: 'HealthCheckPayload'
    service_name = betterproto.string_field(5)
    service_name: str
    request_headers_to_add = betterproto.message_field(6)
    request_headers_to_add: List['HeaderValueOption']
    request_headers_to_remove = betterproto.string_field(8)
    request_headers_to_remove: List[str]
    use_http2 = betterproto.bool_field(7)
    use_http2: bool
    expected_statuses = betterproto.message_field(9)
    expected_statuses: List[type.Int64Range]
    codec_client_type = betterproto.enum_field(10)
    codec_client_type: type.CodecClientType
    service_name_matcher = betterproto.message_field(11)
    service_name_matcher: matcher.StringMatcher


@dataclass
class HealthCheckTcpHealthCheck(betterproto.Message):
    send = betterproto.message_field(1)
    send: 'HealthCheckPayload'
    receive = betterproto.message_field(2)
    receive: List['HealthCheckPayload']


@dataclass
class HealthCheckRedisHealthCheck(betterproto.Message):
    key = betterproto.string_field(1)
    key: str


@dataclass
class HealthCheckGrpcHealthCheck(betterproto.Message):
    __doc__ = '\n    `grpc.health.v1.Health <https://github.com/grpc/grpc/blob/master/src/proto/\n    grpc/health/v1/health.proto>`_-based healthcheck. See `gRPC doc\n    <https://github.com/grpc/grpc/blob/master/doc/health-checking.md>`_ for\n    details.\n    '
    service_name = betterproto.string_field(1)
    service_name: str
    authority = betterproto.string_field(2)
    authority: str


@dataclass
class HealthCheckCustomHealthCheck(betterproto.Message):
    __doc__ = 'Custom health check.'
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class HealthCheckTlsOptions(betterproto.Message):
    __doc__ = '\n    Health checks occur over the transport socket specified for the cluster.\n    This implies that if a cluster is using a TLS-enabled transport socket, the\n    health check will also occur over TLS. This allows overriding the cluster\n    TLS settings, just for health check connections.\n    '
    alpn_protocols = betterproto.string_field(1)
    alpn_protocols: List[str]


@dataclass
class TcpProtocolOptions(betterproto.Message):
    __doc__ = '[#not-implemented-hide:]'


@dataclass
class UpstreamHttpProtocolOptions(betterproto.Message):
    auto_sni = betterproto.bool_field(1)
    auto_sni: bool


@dataclass
class HttpProtocolOptions(betterproto.Message):
    idle_timeout = betterproto.message_field(1)
    idle_timeout: timedelta
    max_connection_duration = betterproto.message_field(3)
    max_connection_duration: timedelta
    max_headers_count = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    max_headers_count: Optional[int]


@dataclass
class Http1ProtocolOptions(betterproto.Message):
    __doc__ = '[#next-free-field: 6]'
    allow_absolute_url = betterproto.message_field(1,
      wraps=(betterproto.TYPE_BOOL))
    allow_absolute_url: Optional[bool]
    accept_http_10 = betterproto.bool_field(2)
    accept_http_10: bool
    default_host_for_http_10 = betterproto.string_field(3)
    default_host_for_http_10: str
    header_key_format = betterproto.message_field(4)
    header_key_format: 'Http1ProtocolOptionsHeaderKeyFormat'
    enable_trailers = betterproto.bool_field(5)
    enable_trailers: bool


@dataclass
class Http1ProtocolOptionsHeaderKeyFormat(betterproto.Message):
    proper_case_words = betterproto.message_field(1,
      group='header_format')
    proper_case_words: 'Http1ProtocolOptionsHeaderKeyFormatProperCaseWords'


@dataclass
class Http1ProtocolOptionsHeaderKeyFormatProperCaseWords(betterproto.Message):
    pass


@dataclass
class Http2ProtocolOptions(betterproto.Message):
    __doc__ = '[#next-free-field: 13]'
    hpack_table_size = betterproto.message_field(1,
      wraps=(betterproto.TYPE_UINT32))
    hpack_table_size: Optional[int]
    max_concurrent_streams = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    max_concurrent_streams: Optional[int]
    initial_stream_window_size = betterproto.message_field(3,
      wraps=(betterproto.TYPE_UINT32))
    initial_stream_window_size: Optional[int]
    initial_connection_window_size = betterproto.message_field(4,
      wraps=(betterproto.TYPE_UINT32))
    initial_connection_window_size: Optional[int]
    allow_connect = betterproto.bool_field(5)
    allow_connect: bool
    allow_metadata = betterproto.bool_field(6)
    allow_metadata: bool
    max_outbound_frames = betterproto.message_field(7,
      wraps=(betterproto.TYPE_UINT32))
    max_outbound_frames: Optional[int]
    max_outbound_control_frames = betterproto.message_field(8,
      wraps=(betterproto.TYPE_UINT32))
    max_outbound_control_frames: Optional[int]
    max_consecutive_inbound_frames_with_empty_payload = betterproto.message_field(9, wraps=(betterproto.TYPE_UINT32))
    max_consecutive_inbound_frames_with_empty_payload: Optional[int]
    max_inbound_priority_frames_per_stream = betterproto.message_field(10,
      wraps=(betterproto.TYPE_UINT32))
    max_inbound_priority_frames_per_stream: Optional[int]
    max_inbound_window_update_frames_per_data_frame_sent = betterproto.message_field(11, wraps=(betterproto.TYPE_UINT32))
    max_inbound_window_update_frames_per_data_frame_sent: Optional[int]
    stream_error_on_invalid_http_messaging = betterproto.bool_field(12)
    stream_error_on_invalid_http_messaging: bool


@dataclass
class GrpcProtocolOptions(betterproto.Message):
    __doc__ = '[#not-implemented-hide:]'
    http2_protocol_options = betterproto.message_field(1)
    http2_protocol_options: 'Http2ProtocolOptions'