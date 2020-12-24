# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/metric_types/counter.py
# Compiled at: 2020-05-04 17:22:35
# Size of source mod 2**32: 2360 bytes
import typing as tp
from .base import EmbeddedSubmetrics, MetricLevel
from .measurable_mixin import MeasurableMixin
from ..data import MetricData, MetricDataCollection
from .registry import register_metric

@register_metric
class CounterMetric(EmbeddedSubmetrics, MeasurableMixin):
    __doc__ = '\n    A counter that can be adjusted by a given value.\n\n    :param sum_children: whether to sum up all calls to children\n    :param count_calls: count the amount of calls to handle()\n    '
    __slots__ = ('sum_children', 'count_calls', 'calls', 'value')
    CLASS_NAME = 'counter'

    def __init__(self, name, root_metric=None, metric_level=None, internal=False, sum_children=True, count_calls=False, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, *args, internal=internal, sum_children=sum_children, count_calls=count_calls, **kwargs)
        self.sum_children = sum_children
        self.count_calls = count_calls
        self.calls = 0
        self.value = 0

    def to_metric_data(self):
        if self.embedded_submetrics_enabled:
            k = super().to_metric_data()
            if self.sum_children:
                k += MetricData(self.name + '.sum', self.value, self.labels, self.get_timestamp(), self.internal)
            if self.count_calls:
                k += MetricData(self.name + '.count', self.calls, self.labels, self.get_timestamp(), self.internal)
            return k
        else:
            p = super().to_metric_data()
            p.set_value(self.value)
            if self.count_calls:
                p += MetricData(self.name + '.count', self.calls, self.labels, self.get_timestamp(), self.internal)
            return p

    def _handle(self, delta=0, **labels):
        if self.embedded_submetrics_enabled or labels:
            if self.sum_children:
                self.value += delta
            self.calls += 1
            return (super()._handle)(delta, **labels)
        self.value += delta
        self.calls += 1