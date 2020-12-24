# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/instrumentation/metrics/metric_types/summary.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 5395 bytes
import collections, warnings, typing as tp, math
from .base import EmbeddedSubmetrics, MetricLevel
from .measurable_mixin import MeasurableMixin
from .registry import register_metric
from ..data import MetricData, MetricDataCollection

def percentile(n: tp.List[float], percent: float) -> float:
    """
    Find the percentile of a list of values.

    :param n: - is a list of values. Note this MUST BE already sorted.
    :param percent: - a float value from 0.0 to 1.0.

    :return: the percentile of the values
    """
    k = (len(n) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return n[int(k)]
    d0 = n[int(f)] * (c - k)
    d1 = n[int(c)] * (k - f)
    return d0 + d1


@register_metric
class SummaryMetric(EmbeddedSubmetrics, MeasurableMixin):
    __doc__ = '\n    A metric that can register some values, sequentially, and then calculate quantiles from it.\n    It calculates configurable quantiles over a sliding window of amount of measurements.\n\n    :param last_calls: last calls to handle() to take into account\n    :param quantiles: a sequence of quantiles to return in to_metric_data\n    :param aggregate_children: whether to sum up children values (if present)\n    :param count_calls: whether to count total amount of calls and total time\n    '
    __slots__ = ('last_calls', 'calls_queue', 'quantiles', 'aggregate_children', 'count_calls',
                 'tot_calls', 'tot_time')
    CLASS_NAME = 'summary'

    def __init__(self, name, root_metric=None, metric_level=None, internal=False, last_calls=100, quantiles=(0.5, 0.95), aggregate_children=True, count_calls=True, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, *args, internal=internal, last_calls=last_calls, 
         quantiles=quantiles, aggregate_children=aggregate_children, 
         count_calls=count_calls, **kwargs)
        self.last_calls = last_calls
        self.calls_queue = collections.deque()
        self.quantiles = quantiles
        self.aggregate_children = aggregate_children
        self.count_calls = count_calls
        self.tot_calls = 0
        self.tot_time = 0

    def _handle(self, time_taken, **labels):
        if self.count_calls:
            self.tot_calls += 1
            self.tot_time += time_taken
        if labels or self.embedded_submetrics_enabled:
            return (super()._handle)(time_taken, **labels)
        if len(self.calls_queue) == self.last_calls:
            self.calls_queue.pop()
        self.calls_queue.appendleft(time_taken)

    def to_metric_data(self) -> MetricDataCollection:
        k = self._to_metric_data()
        if self.count_calls:
            k += MetricData(self.name + '.count', self.tot_calls, self.labels, self.get_timestamp(), self.internal)
            k += MetricData(self.name + '.sum', self.tot_time, self.labels, self.get_timestamp(), self.internal)
        return k

    def _to_metric_data(self):
        if self.embedded_submetrics_enabled:
            k = super().to_metric_data()
            if self.aggregate_children:
                total_calls = []
                for child in self.children:
                    total_calls.extend(child.calls_queue)

                total_calls.sort()
                q = self.calculate_quantiles(total_calls)
                q.postfix_with('total')
                k += q
            if self.count_calls:
                k += MetricData(self.name + '.count', self.tot_calls, self.labels, self.get_timestamp(), self.internal)
                k += MetricData(self.name + '.sum', self.tot_time, self.labels, self.get_timestamp(), self.internal)
            return k
        return self.calculate_quantiles(self.calls_queue)

    def calculate_quantiles(self, calls_queue) -> MetricDataCollection:
        output = MetricDataCollection()
        sorted_calls = sorted(calls_queue)
        for p_val in self.quantiles:
            if not sorted_calls:
                output += MetricData(self.name, 0.0, {**{'quantile': p_val}, **(self.labels)}, self.get_timestamp(), self.internal)
            else:
                output += MetricData(self.name, percentile(sorted_calls, p_val), {**{'quantile': p_val}, **(self.labels)}, self.get_timestamp(), self.internal)

        return output


@register_metric
class QuantileMetric(SummaryMetric):
    CLASS_NAME = 'quantile'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        warnings.warn('quantile is deprecated; use summary instead', DeprecationWarning)