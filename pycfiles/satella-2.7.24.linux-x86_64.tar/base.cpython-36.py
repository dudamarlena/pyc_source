# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/metric_types/base.py
# Compiled at: 2020-05-12 15:04:16
# Size of source mod 2**32: 8692 bytes
import enum, time, typing as tp
from satella.coding.decorators import for_argument
from ..data import MetricData, MetricDataCollection

class MetricLevel(enum.IntEnum):
    DISABLED = 1
    RUNTIME = 2
    DEBUG = 3
    INHERIT = 4

    def __ge__(self, other: 'MetricLevel') -> bool:
        return self.value >= other.value


DISABLED = MetricLevel.DISABLED
RUNTIME = MetricLevel.RUNTIME
DEBUG = MetricLevel.DEBUG
INHERIT = MetricLevel.INHERIT

class Metric:
    __doc__ = "\n    Container for child metrics. A base metric class, as well as the default metric.\n\n    Switch levels by setting metric.level to a proper value\n\n    :param enable_timestamp: append timestamp of last update to the metric\n    :param internal: if True, this metric won't be visible in exporters\n    "
    __slots__ = ('name', 'root_metric', 'internal', '_level', 'enable_timestamp', 'last_updated',
                 'children')
    CLASS_NAME = 'base'

    def get_fully_qualified_name(self):
        data = []
        metric = self
        while metric.root_metric is not None:
            data.append(metric.name)
            metric = metric.root_metric

        return '.'.join(reversed(data))

    def reset(self) -> None:
        """
        Delete all child metrics that this metric contains.

        Also, if called on root metric, sets the runlevel to RUNTIME
        """
        from satella.instrumentation import metrics
        if self.name == '':
            with metrics.metrics_lock:
                metrics.metrics = {}
                metrics.level = MetricLevel.RUNTIME
        else:
            with metrics.metrics_lock:
                metrics.metrics = {k:v for k, v in metrics.metrics.items() if not k.startswith(self.get_fully_qualified_name() + '.')}
                del metrics.metrics[self.get_fully_qualified_name()]
        self.children = []

    def __init__(self, name, root_metric: 'Metric'=None, metric_level: tp.Optional[tp.Union[(MetricLevel, int)]]=None, internal: bool=False, *args, **kwargs):
        """When reimplementing the method, remember to pass kwargs here!"""
        self.name = name
        self.root_metric = root_metric
        self.internal = internal
        if metric_level is None:
            if self.name == '':
                metric_level = MetricLevel.RUNTIME
            else:
                metric_level = MetricLevel.INHERIT
        else:
            self._level = MetricLevel(metric_level)
            self.enable_timestamp = kwargs.get('enable_timestamp', False)
            self.last_updated = time.time() if self.enable_timestamp else None
            assert not (self.name == '' and self.level == MetricLevel.INHERIT), 'Unable to set INHERIT for root metric!'
        self.children = []

    def get_timestamp(self) -> tp.Optional[float]:
        """Return this timestamp, or None if no timestamp support is enabled"""
        if self.enable_timestamp:
            return self.last_updated

    def __str__(self) -> str:
        return self.name

    @property
    def level(self) -> MetricLevel:
        metric = self
        while metric._level == MetricLevel.INHERIT:
            metric = metric.root_metric

        return metric._level

    @level.setter
    @for_argument(None, MetricLevel)
    def level(self, value: MetricLevel) -> None:
        assert not (value == MetricLevel.INHERIT and self.name == ''), 'Cannot set INHERIT for the root metric!'
        self._level = value

    def append_child(self, metric: 'Metric'):
        self.children.append(metric)

    def can_process_this_level(self, target_level: MetricLevel) -> bool:
        return self.level >= target_level

    def to_metric_data(self) -> MetricDataCollection:
        output = MetricDataCollection()
        for child in self.children:
            output += child.to_metric_data()

        output.prefix_with(self.name)
        if self.enable_timestamp:
            output.set_timestamp(self.last_updated)
        return output

    def _handle(self, *args, **kwargs) -> None:
        """
        To be overridden!

        The right place to process your data, after it's level was verified by :meth:`Metric.handle`
        """
        raise TypeError('This is a container metric!')

    @for_argument(None, MetricLevel)
    def handle(self, level: tp.Union[(int, MetricLevel)], *args, **kwargs) -> None:
        if self.can_process_this_level(level):
            if self.enable_timestamp:
                self.last_updated = time.time()
            return (self._handle)(*args, **kwargs)

    def debug(self, *args, **kwargs):
        (self.handle)(MetricLevel.DEBUG, *args, **kwargs)

    def runtime(self, *args, **kwargs):
        (self.handle)(MetricLevel.RUNTIME, *args, **kwargs)


class LeafMetric(Metric):
    __doc__ = '\n    A metric capable of generating only leaf entries.\n\n    You cannot hook up any children to a leaf metric.\n    '
    __slots__ = ('labels', )

    def __init__(self, name, root_metric=None, metric_level=None, labels=None, internal=False, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, internal, *args, **kwargs)
        self.labels = labels or {}
        assert '_timestamp' not in self.labels, 'Cannot make a label called _timestamp!'

    def to_metric_data(self) -> MetricDataCollection:
        return MetricDataCollection(MetricData((self.name), None, (self.labels), internal=(self.internal)))

    def append_child(self, metric: 'Metric'):
        raise TypeError('This metric cannot contain children!')


class EmbeddedSubmetrics(LeafMetric):
    __doc__ = "\n    A metric that can optionally accept some labels in it's handle, and this will be counted as a\n    separate metric.\n    For example:\n\n    >>> metric = getMetric('root.test.IntValue', 'int', enable_timestamp=False)\n    >>> metric.handle(2, label='key')\n    >>> metric.handle(3, label='value')\n\n    If you try to inherit from it, refer to :py:class:`.simple.IntegerMetric` to see how to do it.\n    All please pass all the arguments received from child class into this constructor, as this\n    constructor actually stores them!\n    Refer to :py:class:`.cps.ClicksPerTimeUnitMetric` on how to do that.\n    "
    __slots__ = ('args', 'kwargs', 'embedded_submetrics_enabled', 'children_mapping')

    def __init__(self, name, root_metric=None, metric_level=None, labels=None, internal=False, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, labels, internal, *args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        self.embedded_submetrics_enabled = False
        self.children_mapping = {}
        self.last_updated = time.time()

    def _handle(self, *args, **labels):
        if self.enable_timestamp:
            self.last_updated = time.time()
        else:
            key = tuple(sorted(labels.items()))
            if key:
                self.embedded_submetrics_enabled = True
            else:
                return
            if key in self.children_mapping:
                (self.children_mapping[key]._handle)(*args)
            else:
                clone = self.clone(labels)
                self.children_mapping[key] = clone
                self.children.append(clone)
                (self.children_mapping[key]._handle)(*args)

    def to_metric_data(self):
        if self.embedded_submetrics_enabled:
            v = MetricDataCollection()
            for child in self.children:
                v = v + child.to_metric_data()

            return v
        else:
            return super().to_metric_data()

    def get_specific_metric_data(self, labels: dict) -> MetricDataCollection:
        """
        Return a MetricDataCollection for a child with given labels
        """
        key = tuple(sorted(labels.items()))
        return self.children_mapping[key].to_metric_data()

    def clone(self, labels: dict) -> 'LeafMetric':
        """
        Return a fresh instance of this metric, with it's parent being set to this metric
        and having a particular set of labels, and being of level INHERIT.
        """
        return (self.__class__)(self.name), self, (MetricLevel.INHERIT), *(self.args, labels=labels, **self.kwargs)