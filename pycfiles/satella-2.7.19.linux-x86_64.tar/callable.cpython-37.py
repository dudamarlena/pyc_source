# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/instrumentation/metrics/metric_types/callable.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 1343 bytes
import typing as tp, time
from ..data import MetricDataCollection, MetricData
from .base import LeafMetric, MetricLevel
from .registry import register_metric

@register_metric
class CallableMetric(LeafMetric):
    __doc__ = "\n    A metric whose value at any given point in time is the result of it's callable.\n\n    :param value_getter: a callable() that returns a float - the current value of this metric.\n        It should be easy and cheap to compute, as this callable will be called each time\n        a snapshot of metric state is requested\n    "
    CLASS_NAME = 'callable'
    __slots__ = ('callable', )

    def __init__(self, name, root_metric=None, metric_level=None, labels=None, internal=False, value_getter=lambda : 0, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, labels, internal, *args, **kwargs)
        self.callable = value_getter

    def _handle(self, *args, **kwargs) -> None:
        raise TypeError('You are not supposed to call this!')

    def to_metric_data(self) -> MetricDataCollection:
        mdc = MetricDataCollection()
        mdc += MetricData(self.name, self.callable(), self.labels, time.time(), self.internal)
        return mdc