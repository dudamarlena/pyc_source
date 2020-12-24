# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/logistics/attribution.py
# Compiled at: 2016-06-30 06:13:10
"""this module implement the metric attribution definition

"""
from collections import namedtuple
Metric = namedtuple('Metric', ['name', 'scope'])
ApdexMetric = namedtuple('ApdexMetric', ['name', 'satisfying', 'tolerating', 'frustrating', 'apdex_t'])
TimeMetric = namedtuple('TimeMetric', ['name', 'scope', 'duration', 'exclusive'])
TracedError = namedtuple('TracedError', ['error_filter_key', 'tracker_type', 'trace_data'])
TracedExternalError = namedtuple('TracedExternalError', ['error_filter_key', 'trace_data', 'tracker_type',
 'status_code'])
RootNode = namedtuple('RootNode', ['start_time', 'request_uri', 'duration', 'name', 'trace_data'])
TraceNode = namedtuple('TraceNode', ['start_time', 'end_time', 'metric_name', 'call_url', 'call_count', 'class_name',
 'method_name', 'params', 'children'])

def node_start_time(root, node):
    return int((node.start_time - root.start_time) * 1000.0)


def node_end_time(root, node):
    return int((node.end_time - root.start_time) * 1000.0)


def node_duration_time(node):
    return int((node.end_time - node.start_time) * 1000.0)