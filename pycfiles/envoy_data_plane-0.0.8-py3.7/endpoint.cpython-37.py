# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/api/v2/endpoint.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 5748 bytes
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from envoy_data_plane.envoy.api.v2 import core

@dataclass
class Endpoint(betterproto.Message):
    __doc__ = 'Upstream host identifier.'
    address = betterproto.message_field(1)
    address: core.Address
    health_check_config = betterproto.message_field(2)
    health_check_config: 'EndpointHealthCheckConfig'


@dataclass
class EndpointHealthCheckConfig(betterproto.Message):
    __doc__ = 'The optional health check configuration.'
    port_value = betterproto.uint32_field(1)
    port_value: int


@dataclass
class LbEndpoint(betterproto.Message):
    __doc__ = 'An Endpoint that Envoy can route traffic to. [#next-free-field: 6]'
    endpoint = betterproto.message_field(1, group='host_identifier')
    endpoint: 'Endpoint'
    endpoint_name = betterproto.string_field(5, group='host_identifier')
    endpoint_name: str
    health_status = betterproto.enum_field(2)
    health_status: core.HealthStatus
    metadata = betterproto.message_field(3)
    metadata: core.Metadata
    load_balancing_weight = betterproto.message_field(4,
      wraps=(betterproto.TYPE_UINT32))
    load_balancing_weight: Optional[int]


@dataclass
class LocalityLbEndpoints(betterproto.Message):
    __doc__ = '\n    A group of endpoints belonging to a Locality. One can have multiple\n    LocalityLbEndpoints for a locality, but this is generally only done if the\n    different groups need to have different load balancing weights or different\n    priorities. [#next-free-field: 7]\n    '
    locality = betterproto.message_field(1)
    locality: core.Locality
    lb_endpoints = betterproto.message_field(2)
    lb_endpoints: List['LbEndpoint']
    load_balancing_weight = betterproto.message_field(3,
      wraps=(betterproto.TYPE_UINT32))
    load_balancing_weight: Optional[int]
    priority = betterproto.uint32_field(5)
    priority: int
    proximity = betterproto.message_field(6,
      wraps=(betterproto.TYPE_UINT32))
    proximity: Optional[int]