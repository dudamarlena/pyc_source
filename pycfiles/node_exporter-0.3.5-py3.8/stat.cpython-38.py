# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/stat.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 561 bytes
from prometheus_client.core import GaugeMetricFamily
from .namespace import NAMESPACE
from .collector import Collector

class StatCollector(Collector):
    name = 'stat'

    def collect(self):
        with open('/proc/stat', 'r') as (f):
            for line in f:
                stat_name = line.split(' ')[0]

            if stat_name == 'btime':
                stat_value = float(line.split(' ')[1])
                yield GaugeMetricFamily(('{}_boot_time_seconds'.format(NAMESPACE)),
                  documentation='', value=stat_value)