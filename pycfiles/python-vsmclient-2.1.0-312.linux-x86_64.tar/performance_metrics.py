# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/performance_metrics.py
# Compiled at: 2016-06-13 14:11:03
"""
Performance Metrics interface.
"""
import urllib
from vsmclient import base

class PerformanceMetrics(base.Resource):
    """Performance metrics of ceph cluster and server of cpu, memory and so on."""

    def __repr__(self):
        return '<PerformanceMetrics: %s>' % self.id


class PerformanceMetricsManager(base.ManagerWithFind):
    """
    Manage :class:`Server` resources.
    """
    resource_class = PerformanceMetrics

    def list(self, search_opts=None):
        """
        Get a list of .
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        ret = self._list('/performance_metrics/get_list%s' % query_string, 'performance_metrics')
        return ret

    def get_metrics(self, search_opts=None):
        """
        Get a list of metrics by metrics name and timestamp.
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        resp, body = self.api.client.get('/performance_metrics/get_metrics%s' % query_string)
        return body

    def get_metrics_all_types(self, search_opts=None):
        """
        Get a list of metrics by metrics name and timestamp.
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        resp, body = self.api.client.get('/performance_metrics/get_metrics_all_types%s' % query_string)
        return body