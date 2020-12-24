# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/olxbr/BarterDude/barterdude/hooks/metrics/prometheus/metrics.py
# Compiled at: 2020-04-29 12:15:10
# Size of source mod 2**32: 1265 bytes
from prometheus_client.metrics import MetricWrapperBase
from prometheus_client import Counter, Gauge, Summary, Histogram, Info, Enum
from functools import partial

class Metrics(dict):

    def __init__(self, registry):
        self._Metrics__registry = registry

    @property
    def counter(self) -> Counter.__class__:
        return partial(Counter, registry=(self._Metrics__registry))

    @property
    def gauge(self) -> Gauge.__class__:
        return partial(Gauge, registry=(self._Metrics__registry))

    @property
    def summary(self) -> Summary.__class__:
        return partial(Summary, registry=(self._Metrics__registry))

    @property
    def histogram(self) -> Histogram.__class__:
        return partial(Histogram, registry=(self._Metrics__registry))

    @property
    def info(self) -> Info.__class__:
        return partial(Info, registry=(self._Metrics__registry))

    @property
    def enum(self) -> Enum.__class__:
        return partial(Enum, registry=(self._Metrics__registry))

    def __setitem__(self, name, metric):
        if name in self:
            value = self.__getitem__(name)
            raise ValueError(f"Key {name} already exists with value {value}")
        super(Metrics, self).__setitem__(name, metric)