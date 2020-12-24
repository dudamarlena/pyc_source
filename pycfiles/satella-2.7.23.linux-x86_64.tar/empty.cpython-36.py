# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/metric_types/empty.py
# Compiled at: 2020-05-08 08:03:23
# Size of source mod 2**32: 547 bytes
from .registry import register_metric
from .base import Metric
from ..data import MetricDataCollection

@register_metric
class EmptyMetric(Metric):
    __doc__ = "\n    A metric that disregards all data that it's fed, and outputs nothing.\n\n    A placeholder for the times when you configure metrics and decide to leave some of them out\n    blank.\n    "
    __slots__ = ()
    CLASS_NAME = 'empty'

    def _handle(self, *args, **kwargs) -> None:
        pass

    def to_metric_data(self) -> MetricDataCollection:
        return MetricDataCollection()