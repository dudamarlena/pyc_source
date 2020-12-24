# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/metric_types/histogram.py
# Compiled at: 2020-05-04 17:22:35
# Size of source mod 2**32: 3788 bytes
import math, typing as tp, itertools
from .base import EmbeddedSubmetrics, MetricLevel
from .measurable_mixin import MeasurableMixin
from .registry import register_metric
from ..data import MetricData, MetricDataCollection

@register_metric
class HistogramMetric(EmbeddedSubmetrics, MeasurableMixin):
    __doc__ = "\n    A histogram, by  `Prometheus' <https://github.com/prometheus/client_python#histogram/>`_\n    interpretation.\n    \n    :param buckets: buckets to add. First bucket will be from zero to first value, second from first\n        value to second, last bucket will be from last value to infinity. So there are \n        len(buckets)+1 buckets. Buckets are expected to be passed in sorted!\n    :param aggregate_children: whether to accept child calls to be later presented as total\n    "
    __slots__ = ('bucket_limits', 'buckets', 'aggregate_children', 'count', 'sum')
    CLASS_NAME = 'histogram'

    def __init__(self, name, root_metric=None, metric_level=None, internal=False, buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0), aggregate_children=True, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, *args, internal=internal, buckets=buckets, aggregate_children=aggregate_children, **kwargs)
        self.bucket_limits = list(buckets)
        self.buckets = [0] * (len(buckets) + 1)
        self.aggregate_children = aggregate_children
        self.count = 0
        self.sum = 0.0

    def _handle(self, value, **labels):
        self.count += 1
        self.sum += value
        if self.embedded_submetrics_enabled or labels:
            (super()._handle)(value, **labels)
            if not self.aggregate_children:
                return
        lower_bound = 0.0
        for index, upper_bound in itertools.chain(enumerate(self.bucket_limits), [
         (
          len(self.bucket_limits), math.inf)]):
            if lower_bound <= value < upper_bound:
                self.buckets[index] += 1
            lower_bound = upper_bound

    def to_metric_data(self):
        if self.embedded_submetrics_enabled:
            k = super().to_metric_data()
            if self.aggregate_children:
                mdc = self.containers_to_metric_data()
                mdc.postfix_with('total')
                mdc += MetricData(self.name + '.total.sum', self.sum, {}, self.get_timestamp())
                mdc += MetricData(self.name + '.total.count', self.count, {}, self.get_timestamp())
                k += mdc
            return k
        else:
            mdc = self.containers_to_metric_data()
            mdc += MetricData(self.name + '.sum', self.sum, self.labels, self.get_timestamp())
            mdc += MetricData(self.name + '.count', self.count, self.labels, self.get_timestamp())
            return mdc

    def containers_to_metric_data(self) -> MetricDataCollection:
        output = []
        lower_bound = 0.0
        for amount, upper_bound in zip(self.buckets, self.bucket_limits + [math.inf]):
            labels = self.labels.copy()
            labels.update(le=upper_bound, ge=lower_bound)
            output.append(MetricData(self.name, amount, labels, self.get_timestamp(), self.internal))
            lower_bound = upper_bound

        return MetricDataCollection(output)