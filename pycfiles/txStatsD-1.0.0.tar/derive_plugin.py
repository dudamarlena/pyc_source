# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sidnei/src/txstatsd/trunk/twisted/plugins/derive_plugin.py
# Compiled at: 2012-05-24 12:31:37
from zope.interface import implements
from twisted.plugin import IPlugin
from txstatsd.itxstatsd import IMetric, IMetricFactory
from txstatsd.metrics.metric import Metric
import logging, time

class DeriveMetricReporter(object):
    """
    A simplier meter metric which measures instant throughput rate for each interval.
    """
    implements(IMetric)

    def __init__(self, name, wall_time_func=time.time, prefix=''):
        """Construct a metric we expect to be periodically updated.

        @param name: Indicates what is being instrumented.
        @param wall_time_func: Function for obtaining wall time.
        """
        self.name = name
        self.wall_time_func = wall_time_func
        if prefix:
            prefix += '.'
        self.prefix = prefix
        self.update = self.count = 0
        self.poll_time = self.wall_time_func()

    def process(self, fields):
        """
        Process new data for this metric.

        @type fields: C{list}
        @param fields: The list of message parts. Usually in the form of
        (value, metric_type, [sample_rate])
        """
        (val, k) = fields
        self.update += float(val)

    def flush(self, interval, timestamp):
        """
        Returns a string with new line separated list of metrics to report.

        @type interval: C{float}
        @param interval: The time since last flush.
        @type timestamp: C{float}
        @param timestamp: The timestamp for now.
        """
        poll_prev, self.poll_time = self.poll_time, self.wall_time_func()
        if self.poll_time == poll_prev:
            return list()
        rate = float(self.update) / (self.poll_time - poll_prev)
        self.count, self.update = self.count + self.update, 0
        return list((self.prefix + self.name + '.' + item, round(value, 6), timestamp) for (item, value) in [
         (
          'count', self.count), ('rate', rate)])


class DeriveMetricFactory(object):
    implements(IMetricFactory, IPlugin)
    name = 'derive'
    metric_type = 'dx'

    def build_metric(self, prefix, name, wall_time_func=None):
        return DeriveMetricReporter(name, prefix=prefix, wall_time_func=wall_time_func)

    def configure(self, options):
        pass


derive_metric_factory = DeriveMetricFactory()