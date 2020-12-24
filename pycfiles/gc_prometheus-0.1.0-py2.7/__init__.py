# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gc_prometheus/__init__.py
# Compiled at: 2015-04-25 15:13:02
import gc, prometheus_client, sys

def set_function_on_map_gauge(gauge, labelvalues, fn):
    for l in labelvalues:

        def get_item(fn=fn, l=l):
            return fn()[l]

        gauge.labels(l).set_function(get_item)


enabled = prometheus_client.Gauge('python_gc_enabled', 'Whether the garbage collector is enabled.')
enabled.set_function(gc.isenabled)
debug = prometheus_client.Gauge('python_gc_debug', 'The debug flags currently set on the Python GC.')
debug.set_function(gc.get_debug)
count = prometheus_client.Gauge('python_gc_count', 'Count of objects tracked by the Python garbage collector, by generation.', [
 'generation'])
set_function_on_map_gauge(count, (0, 1, 2), gc.get_count)
thresholds = prometheus_client.Gauge('python_gc_threshold', 'GC thresholds by generation', [
 'generation'])
set_function_on_map_gauge(thresholds, (0, 1, 2), gc.get_threshold)
if sys.version_info >= (3, 4):
    collections = prometheus_client.Gauge('python_gc_collections_total', 'Number of GC collections that occurred by generation', [
     'generation'])
    set_function_on_map_gauge(collections, (0, 1, 2), lambda : [ x['collections'] for x in gc.get_stats() ])
    collected = prometheus_client.Gauge('python_gc_collected_total', 'Number of garbage collected objects by generation', [
     'generation'])
    set_function_on_map_gauge(collected, (0, 1, 2), lambda : [ x['collected'] for x in gc.get_stats() ])
    uncollectables = prometheus_client.Gauge('python_gc_uncollectables', 'Number of uncollectable objects by generation', [
     'generation'])
    set_function_on_map_gauge(uncollectables, (0, 1, 2), lambda : [ x['uncollectable'] for x in gc.get_stats() ])