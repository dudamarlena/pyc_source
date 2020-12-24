# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sidnei/src/txstatsd/trunk/twisted/plugins/distinct_plugin.py
# Compiled at: 2012-06-28 13:21:19
from zope.interface import implements
from twisted.plugin import IPlugin
from txstatsd.itxstatsd import IMetricFactory
from txstatsd.metrics.distinctmetric import DistinctMetricReporter

class DistinctMetricFactory(object):
    implements(IMetricFactory, IPlugin)
    name = 'pdistinct'
    metric_type = 'pd'

    def build_metric(self, prefix, name, wall_time_func=None):
        return DistinctMetricReporter(name, prefix=prefix, wall_time_func=wall_time_func)

    def configure(self, options):
        pass


distinct_metric_factory = DistinctMetricFactory()