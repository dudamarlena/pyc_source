# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gc_prometheus/profile.py
# Compiled at: 2015-04-25 15:14:26
import gc, gc_prometheus, prometheus_client, sys, time
if sys.version_info < (3, 3):
    raise ImportError('gc_prometheus.profile is only available for Python >=3.3')
collection_total = prometheus_client.Gauge('python_gc_collection_process_time_total_s', 'Total process time spent in garbage collection')

class GcProfiler(object):

    def __init__(self):
        self.last_collection_start = None
        return

    def Now(self):
        return time.process_time()

    def UpdateMetrics(self, interval):
        collection_total.inc(interval)

    def Callback(self, phase, info):
        if phase == 'start':
            self.last_collection_start = self.Now()
        elif phase == 'stop':
            now = self.Now()
            self.UpdateMetrics(now - self.last_collection_start)


profiler = GcProfiler()
gc.callbacks.append(profiler.Callback)