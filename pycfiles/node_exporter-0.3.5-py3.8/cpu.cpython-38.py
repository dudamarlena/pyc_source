# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/cpu.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 1554 bytes
from re import match, search
from prometheus_client.core import CounterMetricFamily
from .namespace import NAMESPACE
from .collector import Collector

class CpuCollector(Collector):
    name = 'cpu'

    def metric(self, metric, value, cpuid, mode):
        metric.add_metric(labels=[cpuid, mode], value=value)

    def collect(self):
        metric = CounterMetricFamily(('{}_{}_seconds_total'.format(NAMESPACE, self.name)),
          'Seconds the cpus spent in each mode.', labels=['cpu', 'mode'])
        with open('/proc/stat', 'r') as (f):
            for line in f:
                s = search('^cpu([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+([0-9]+)\\s+', line)

            if s:
                cpuid, user, nice, system, idle, iowait, irq, softirq, steal = (
                 s.group(1), s.group(2), s.group(3), s.group(4),
                 s.group(5), s.group(6), s.group(7), s.group(8), s.group(9))
                self.metric(metric, float(user), cpuid, 'user')
                self.metric(metric, float(nice), cpuid, 'nice')
                self.metric(metric, float(system), cpuid, 'system')
                self.metric(metric, float(idle), cpuid, 'idle')
                self.metric(metric, float(iowait), cpuid, 'iowait')
                self.metric(metric, float(irq), cpuid, 'irq')
                self.metric(metric, float(softirq), cpuid, 'softirq')
                self.metric(metric, float(steal), cpuid, 'steal')
        yield metric