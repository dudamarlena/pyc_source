# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/api/v2/cluster.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 13286 bytes
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional
import betterproto
from envoy_data_plane.envoy import type
from envoy_data_plane.envoy.api.v2 import core
from envoy_data_plane.google import protobuf

@dataclass
class CircuitBreakers(betterproto.Message):
    __doc__ = '\n    :ref:`Circuit breaking<arch_overview_circuit_break>` settings can be\n    specified individually for each defined priority.\n    '
    thresholds = betterproto.message_field(1)
    thresholds: List['CircuitBreakersThresholds']


@dataclass
class CircuitBreakersThresholds(betterproto.Message):
    __doc__ = '\n    A Thresholds defines CircuitBreaker settings for a\n    :ref:`RoutingPriority<envoy_api_enum_core.RoutingPriority>`. [#next-free-\n    field: 9]\n    '
    priority = betterproto.enum_field(1)
    priority: core.RoutingPriority
    max_connections = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    max_connections: Optional[int]
    max_pending_requests = betterproto.message_field(3,
      wraps=(betterproto.TYPE_UINT32))
    max_pending_requests: Optional[int]
    max_requests = betterproto.message_field(4,
      wraps=(betterproto.TYPE_UINT32))
    max_requests: Optional[int]
    max_retries = betterproto.message_field(5,
      wraps=(betterproto.TYPE_UINT32))
    max_retries: Optional[int]
    retry_budget = betterproto.message_field(8)
    retry_budget: 'CircuitBreakersThresholdsRetryBudget'
    track_remaining = betterproto.bool_field(6)
    track_remaining: bool
    max_connection_pools = betterproto.message_field(7,
      wraps=(betterproto.TYPE_UINT32))
    max_connection_pools: Optional[int]


@dataclass
class CircuitBreakersThresholdsRetryBudget(betterproto.Message):
    budget_percent = betterproto.message_field(1)
    budget_percent: type.Percent
    min_retry_concurrency = betterproto.message_field(2,
      wraps=(betterproto.TYPE_UINT32))
    min_retry_concurrency: Optional[int]


@dataclass
class Filter(betterproto.Message):
    name = betterproto.string_field(1)
    name: str
    typed_config = betterproto.message_field(2)
    typed_config: protobuf.Any


@dataclass
class OutlierDetection(betterproto.Message):
    __doc__ = '\n    See the :ref:`architecture overview <arch_overview_outlier_detection>` for\n    more information on outlier detection. [#next-free-field: 21]\n    '
    consecutive_5xx = betterproto.message_field(1,
      wraps=(betterproto.TYPE_UINT32))
    consecutive_5xx: Optional[int]
    interval = betterproto.message_field(2)
    interval: timedelta
    base_ejection_time = betterproto.message_field(3)
    base_ejection_time: timedelta
    max_ejection_percent = betterproto.message_field(4,
      wraps=(betterproto.TYPE_UINT32))
    max_ejection_percent: Optional[int]
    enforcing_consecutive_5xx = betterproto.message_field(5,
      wraps=(betterproto.TYPE_UINT32))
    enforcing_consecutive_5xx: Optional[int]
    enforcing_success_rate = betterproto.message_field(6,
      wraps=(betterproto.TYPE_UINT32))
    enforcing_success_rate: Optional[int]
    success_rate_minimum_hosts = betterproto.message_field(7,
      wraps=(betterproto.TYPE_UINT32))
    success_rate_minimum_hosts: Optional[int]
    success_rate_request_volume = betterproto.message_field(8,
      wraps=(betterproto.TYPE_UINT32))
    success_rate_request_volume: Optional[int]
    success_rate_stdev_factor = betterproto.message_field(9,
      wraps=(betterproto.TYPE_UINT32))
    success_rate_stdev_factor: Optional[int]
    consecutive_gateway_failure = betterproto.message_field(10,
      wraps=(betterproto.TYPE_UINT32))
    consecutive_gateway_failure: Optional[int]
    enforcing_consecutive_gateway_failure = betterproto.message_field(11,
      wraps=(betterproto.TYPE_UINT32))
    enforcing_consecutive_gateway_failure: Optional[int]
    split_external_local_origin_errors = betterproto.bool_field(12)
    split_external_local_origin_errors: bool
    consecutive_local_origin_failure = betterproto.message_field(13,
      wraps=(betterproto.TYPE_UINT32))
    consecutive_local_origin_failure: Optional[int]
    enforcing_consecutive_local_origin_failure = betterproto.message_field(14, wraps=(betterproto.TYPE_UINT32))
    enforcing_consecutive_local_origin_failure: Optional[int]
    enforcing_local_origin_success_rate = betterproto.message_field(15,
      wraps=(betterproto.TYPE_UINT32))
    enforcing_local_origin_success_rate: Optional[int]
    failure_percentage_threshold = betterproto.message_field(16,
      wraps=(betterproto.TYPE_UINT32))
    failure_percentage_threshold: Optional[int]
    enforcing_failure_percentage = betterproto.message_field(17,
      wraps=(betterproto.TYPE_UINT32))
    enforcing_failure_percentage: Optional[int]
    enforcing_failure_percentage_local_origin = betterproto.message_field(18, wraps=(betterproto.TYPE_UINT32))
    enforcing_failure_percentage_local_origin: Optional[int]
    failure_percentage_minimum_hosts = betterproto.message_field(19,
      wraps=(betterproto.TYPE_UINT32))
    failure_percentage_minimum_hosts: Optional[int]
    failure_percentage_request_volume = betterproto.message_field(20,
      wraps=(betterproto.TYPE_UINT32))
    failure_percentage_request_volume: Optional[int]