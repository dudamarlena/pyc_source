# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/meminfo.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 1138 bytes
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from .namespace import NAMESPACE
from .collector import Collector

def parseMemInfo(lines):
    meminfo = {}
    for l in lines:
        parts = re.split('\\s+', l)
        value = float(parts[1])
        key = parts[0][0:-1]
        m = re.search('\\((.*)\\)', key)
        if m:
            key = re.sub('\\((.*)\\)', m.group(1), key)
        if len(parts) >= 3:
            value *= 1024
            key = '{}_bytes'.format(key)
        meminfo[key.lower()] = value
    else:
        return meminfo


class MeminfoCollector(Collector):
    name = 'memory'

    def collect(self):
        with open('/proc/meminfo', 'r') as (f):
            meminfo = parseMemInfo(f)
        for k, v in meminfo.items():
            if k.endswith('_total'):
                m = CounterMetricFamily(('{}_{}_{}'.format(NAMESPACE, self.name, k)),
                  value=v, documentation='')
            else:
                m = GaugeMetricFamily(('{}_{}_{}'.format(NAMESPACE, self.name, k)),
                  value=v, documentation='')
            (yield m)