# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/diskstats.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 2395 bytes
import re
from prometheus_client.core import CounterMetricFamily
from .namespace import NAMESPACE
from .collector import Collector
ignored_devies = '^(ram|loop|fd|(h|s|v|xv)d[a-z]|nvme\\d+n\\d+p)\\d+$'
factors = [1, 1, 1, 0.001, 1, 1, 1, 0.001, 1, 0.001, 0.001]

def parseDiskStats(lines, name):
    ms = [
     CounterMetricFamily(('{}_{}_reads_completed_total'.format(NAMESPACE, name)), documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_reads_merged_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_read_bytes_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_read_time_seconds_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_writes_completed_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_writes_merged_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_writes_bytes_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_writes_time_seconds_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_io_now'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_io_time_seconds_total'.format(NAMESPACE, name)),
       documentation='', labels=['device']),
     CounterMetricFamily(('{}_{}_io_time_weighted_seconds_total'.format(NAMESPACE, name)), documentation='', labels=['device'])]
    for line in lines:
        parts = re.split('\\s+', line)
        if len(parts) >= 5:
            dev = parts[3]
            if re.match(ignored_devies, dev) is None:
                stats = parts[4:]
                for i, val in enumerate(stats):
                    if i < len(ms):
                        value = float(val) * factors[i]
                        ms[i].add_metric([dev], value)

        return ms


class DiskstatsCollector(Collector):
    name = 'disk'

    def collect(self):
        with open('/proc/diskstats', 'r') as (f):
            for m in parseDiskStats(f, self.name):
                (yield m)