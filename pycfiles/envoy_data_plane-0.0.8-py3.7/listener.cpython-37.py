# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/api/v2/listener.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 12015 bytes
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from envoy_data_plane.envoy import type
from envoy_data_plane.envoy.api.v2 import auth
from envoy_data_plane.envoy.api.v2 import core
from envoy_data_plane.google import protobuf

class FilterChainMatchConnectionSourceType(betterproto.Enum):
    ANY = 0
    LOCAL = 1
    EXTERNAL = 2


@dataclass
class Filter(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(4, group='config_type')
    typed_config: protobuf.Any


@dataclass
class FilterChainMatch(betterproto.Message):
    __doc__ = "\n    Specifies the match criteria for selecting a specific filter chain for a\n    listener. In order for a filter chain to be selected, *ALL* of its criteria\n    must be fulfilled by the incoming connection, properties of which are set\n    by the networking stack and/or listener filters. The following order\n    applies: 1. Destination port. 2. Destination IP address. 3. Server name\n    (e.g. SNI for TLS protocol), 4. Transport protocol. 5. Application\n    protocols (e.g. ALPN for TLS protocol). 6. Source type (e.g. any, local or\n    external network). 7. Source IP address. 8. Source port. For criteria that\n    allow ranges or wildcards, the most specific value in any of the configured\n    filter chains that matches the incoming connection is going to be used\n    (e.g. for SNI ``www.example.com`` the most specific match would be\n    ``www.example.com``, then ``*.example.com``, then ``*.com``, then any\n    filter chain without ``server_names`` requirements). [#comment: Implemented\n    rules are kept in the preference order, with deprecated fields listed at\n    the end, because that's how we want to list them in the docs.\n    [#comment:TODO(PiotrSikora): Add support for configurable precedence of the\n    rules] [#next-free-field: 13]\n    "
    destination_port = betterproto.message_field(8,
      wraps=(betterproto.TYPE_UINT32))
    destination_port: Optional[int]
    prefix_ranges = betterproto.message_field(3)
    prefix_ranges: List[core.CidrRange]
    address_suffix = betterproto.string_field(4)
    address_suffix: str
    suffix_len = betterproto.message_field(5,
      wraps=(betterproto.TYPE_UINT32))
    suffix_len: Optional[int]
    source_type = betterproto.enum_field(12)
    source_type: 'FilterChainMatchConnectionSourceType'
    source_prefix_ranges = betterproto.message_field(6)
    source_prefix_ranges: List[core.CidrRange]
    source_ports = betterproto.uint32_field(7)
    source_ports: List[int]
    server_names = betterproto.string_field(11)
    server_names: List[str]
    transport_protocol = betterproto.string_field(9)
    transport_protocol: str
    application_protocols = betterproto.string_field(10)
    application_protocols: List[str]


@dataclass
class FilterChain(betterproto.Message):
    __doc__ = '\n    A filter chain wraps a set of match criteria, an option TLS context, a set\n    of filters, and various other parameters. [#next-free-field: 8]\n    '
    filter_chain_match = betterproto.message_field(1)
    filter_chain_match: 'FilterChainMatch'
    tls_context = betterproto.message_field(2)
    tls_context: auth.DownstreamTlsContext
    filters = betterproto.message_field(3)
    filters: List['Filter']
    use_proxy_proto = betterproto.message_field(4,
      wraps=(betterproto.TYPE_BOOL))
    use_proxy_proto: Optional[bool]
    metadata = betterproto.message_field(5)
    metadata: core.Metadata
    transport_socket = betterproto.message_field(6)
    transport_socket: core.TransportSocket
    name = betterproto.string_field(7)
    name: str


@dataclass
class ListenerFilterChainMatchPredicate(betterproto.Message):
    __doc__ = '\n    [#not-implemented-hide:] Listener filter chain match configuration. This is\n    a recursive structure which allows complex nested match configurations to\n    be built using various logical operators. [#next-free-field: 6]\n    '
    or_match = betterproto.message_field(1,
      group='rule')
    or_match: 'ListenerFilterChainMatchPredicateMatchSet'
    and_match = betterproto.message_field(2,
      group='rule')
    and_match: 'ListenerFilterChainMatchPredicateMatchSet'
    not_match = betterproto.message_field(3,
      group='rule')
    not_match: 'ListenerFilterChainMatchPredicate'
    any_match = betterproto.bool_field(4, group='rule')
    any_match: bool
    destination_port_range = betterproto.message_field(5, group='rule')
    destination_port_range: type.Int32Range


@dataclass
class ListenerFilterChainMatchPredicateMatchSet(betterproto.Message):
    __doc__ = 'A set of match configurations used for logical operations.'
    rules = betterproto.message_field(1)
    rules: List['ListenerFilterChainMatchPredicate']


@dataclass
class ListenerFilter(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any
    filter_disabled = betterproto.message_field(4)
    filter_disabled: 'ListenerFilterChainMatchPredicate'


@dataclass
class UdpListenerConfig(betterproto.Message):
    udp_listener_name = betterproto.string_field(1)
    udp_listener_name: str
    config = betterproto.message_field(2, group='config_type')
    config: protobuf.Struct
    typed_config = betterproto.message_field(3, group='config_type')
    typed_config: protobuf.Any


@dataclass
class ActiveRawUdpListenerConfig(betterproto.Message):
    pass