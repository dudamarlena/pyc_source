# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/loadavg.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 473 bytes
from prometheus_client.core import GaugeMetricFamily
from .namespace import NAMESPACE
from .collector import Collector

def parseLoad(data):
    return float(data.split(' ')[0])


class LoadavgCollector(Collector):
    name = 'loadavg'

    def collect(self):
        with open('/proc/loadavg', 'r') as (f):
            load1_val = parseLoad(f.readline())
        (yield GaugeMetricFamily(('{}_load1'.format(NAMESPACE)),
          documentation='', value=(float(load1_val))))