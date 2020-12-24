# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/metric_types/simple.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 1177 bytes
import typing as tp
from .base import EmbeddedSubmetrics
from .measurable_mixin import MeasurableMixin
from .registry import register_metric
from ..data import MetricData, MetricDataCollection

class SimpleMetric(EmbeddedSubmetrics):
    __slots__ = ('data', )
    CLASS_NAME = 'string'
    CONSTRUCTOR = str

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.data = None

    def _handle(self, value, **labels):
        if self.embedded_submetrics_enabled or labels:
            return (super()._handle)(value, **labels)
        self.data = self.CONSTRUCTOR(value)

    def to_metric_data(self):
        if self.embedded_submetrics_enabled:
            return super().to_metric_data()
        else:
            return MetricDataCollection(MetricData(self.name, self.data, self.labels, self.get_timestamp(), self.internal))


@register_metric
class IntegerMetric(SimpleMetric):
    CLASS_NAME = 'int'
    CONSTRUCTOR = int


@register_metric
class FloatMetric(SimpleMetric, MeasurableMixin):
    CLASS_NAME = 'float'
    CONSTRUCTOR = float