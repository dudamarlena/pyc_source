# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/instrumentation/metrics/metric_types/cps.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 2964 bytes
import collections, time, typing as tp
from .base import EmbeddedSubmetrics
from .registry import register_metric
from ..data import MetricData, MetricDataCollection

@register_metric
class ClicksPerTimeUnitMetric(EmbeddedSubmetrics):
    __doc__ = '\n    This tracks the amount of calls to handle() during the last time periods, as specified by time_unit_vectors\n    (in seconds). You may specify multiple time periods as consequent entries in the list.\n\n    By default (if you do not specify otherwise) this will track calls made during the last second.\n    '
    __slots__ = ('last_clicks', 'aggregate_children', 'cutoff_period', 'time_unit_vectors')
    CLASS_NAME = 'cps'

    def __init__(self, *args, time_unit_vectors=None, aggregate_children=True, internal=False, **kwargs):
        (super().__init__)(args, internal=internal, time_unit_vectors=time_unit_vectors, **kwargs)
        time_unit_vectors = time_unit_vectors or [1]
        self.last_clicks = collections.deque()
        self.aggregate_children = aggregate_children
        self.cutoff_period = max(time_unit_vectors)
        self.time_unit_vectors = time_unit_vectors

    def _handle(self, **labels):
        if labels or self.embedded_submetrics_enabled:
            return (super()._handle)(**labels)
        mono_time = time.monotonic()
        self.last_clicks.append(time.monotonic())
        try:
            while self.last_clicks[0] <= mono_time - self.cutoff_period:
                self.last_clicks.popleft()

        except IndexError:
            pass

    def to_metric_data(self):
        if self.embedded_submetrics_enabled:
            k = super().to_metric_data()
            if not self.aggregate_children:
                return k
            last_clicks = []
            for child in self.children:
                last_clicks.extend(child.last_clicks)

            sum_data = self.count_vectors(last_clicks)
            sum_data.postfix_with('total')
            return k + sum_data
        return self.count_vectors(self.last_clicks)

    def count_vectors(self, last_clicks) -> MetricDataCollection:
        count_map = [0] * len(self.time_unit_vectors)
        mono_time = time.monotonic()
        time_unit_vectors = [mono_time - v for v in self.time_unit_vectors]
        for v in last_clicks:
            for index, cutoff in enumerate(time_unit_vectors):
                if v >= cutoff:
                    count_map[index] += 1

        output = []
        for time_unit, count in zip(self.time_unit_vectors, count_map):
            output.append(MetricData(self.name, count, {**{'period': time_unit}, **(self.labels)}, self.get_timestamp(), self.internal))

        return MetricDataCollection(output)