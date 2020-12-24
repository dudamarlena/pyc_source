# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/instrumentation/metrics/aggregate.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 1201 bytes
import typing as tp
from .metric_types import Metric, MetricLevel
from metric_types.measurable_mixin import MeasurableMixin

class AggregateMetric(Metric, MeasurableMixin):
    __doc__ = "\n    A virtual metric grabbing a few other metrics and having a single .handle() call represent a bunch of\n    calls to other metrics. Ie, the following:\n\n    >>> m1 = getMetric('summary', 'summary')\n    >>> m2 = getMetric('histogram', 'histogram')\n    >>> m1.runtime()\n    >>> m2.runtime()\n\n    Is the same as:\n\n    >>> am = AggregateMetric(getMetric('summary', 'summary'), getMetric('histogram', 'histogram'))\n    >>> am.runtime()\n\n    Note that this class supports only reporting. It doesn't read data, or read/write metric levels.\n    "
    __slots__ = ('metrics', )

    def __init__(self, *metrics):
        self.metrics = metrics

    def handle(self, level: tp.Union[(int, MetricLevel)], *args, **kwargs) -> None:
        for metric in self.metrics:
            (metric.handle)(level, *args, **kwargs)

    def debug(self, *args, **kwargs) -> None:
        (self.handle)(MetricLevel.DEBUG, *args, **kwargs)

    def runtime(self, *args, **kwargs) -> None:
        (self.handle)(MetricLevel.RUNTIME, *args, **kwargs)