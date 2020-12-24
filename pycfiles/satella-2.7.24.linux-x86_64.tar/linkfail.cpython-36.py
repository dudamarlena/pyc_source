# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/metrics/metric_types/linkfail.py
# Compiled at: 2020-05-12 15:04:16
# Size of source mod 2**32: 4506 bytes
import typing as tp
from ..data import MetricDataCollection, MetricData
from .base import EmbeddedSubmetrics, MetricLevel
from .registry import register_metric
import collections

@register_metric
class LinkfailMetric(EmbeddedSubmetrics):
    __doc__ = '\n    Metric that measures whether given link is operable.\n\n    :param consecutive_failures_to_offline: consecutive failures needed for link to become offline\n    :param consecutive_successes_to_online: consecutive successes needed for link to become online\n        after a failure\n    :param callback_on_online: callback that accepts an address of a link that becomes online\n        and labels\n    :param callback_on_offline: callback that accepts an address of a link that becomes offline\n        and labels\n    '
    __slots__ = ('working', 'consecutive_failures', 'consecutive_successes', 'callback_on_online',
                 'callback_on_offline', 'consecutive_failures_to_offline', 'consecutive_successes_to_online')
    CLASS_NAME = 'linkfail'

    def __init__(self, name, root_metric=None, metric_level=None, labels=None, internal=False, consecutive_failures_to_offline=100, consecutive_successes_to_online=10, callback_on_online=lambda a, b: None, callback_on_offline=lambda a, b: None, *args, **kwargs):
        (super().__init__)(name, root_metric, metric_level, labels, internal, *args, consecutive_failures_to_offline=consecutive_failures_to_offline, 
         consecutive_successes_to_online=consecutive_successes_to_online, 
         callback_on_offline=callback_on_offline, 
         callback_on_online=callback_on_online, **kwargs)
        self.working = collections.defaultdict(lambda : True)
        self.consecutive_failures = collections.defaultdict(lambda : 0)
        self.consecutive_successes = collections.defaultdict(lambda : 0)
        self.callback_on_online = callback_on_online
        self.callback_on_offline = callback_on_offline
        self.consecutive_failures_to_offline = consecutive_failures_to_offline
        self.consecutive_successes_to_online = consecutive_successes_to_online

    def _handle(self, success, address=0, *args, **labels):
        if self.embedded_submetrics_enabled or labels:
            return (super()._handle)(success, *args, address=address, **labels)
        if success:
            self.consecutive_failures[address] = 0
            self.consecutive_successes[address] += 1
            if not self.working[address]:
                if self.consecutive_successes[address] == self.consecutive_successes_to_online:
                    self.working[address] = True
                    self.callback_on_online(address, self.labels)
        else:
            self.consecutive_failures[address] += 1
            self.consecutive_successes[address] = 0
        if self.working[address]:
            if self.consecutive_failures[address] == self.consecutive_failures_to_offline:
                self.working[address] = False
                self.callback_on_offline(address, self.labels)

    def to_metric_data(self) -> MetricDataCollection:
        mdc = MetricDataCollection()
        keys = set(self.consecutive_successes.keys())
        keys = keys.union(set(self.consecutive_failures.keys()))
        for address in keys:
            labels = self.labels.copy()
            if keys != {0}:
                labels.update(address=address)
            mdc += MetricData(self.name + '.consecutive_failures', self.consecutive_failures[address], labels, self.get_timestamp(), self.internal)
            mdc += MetricData(self.name + '.consecutive_successes', self.consecutive_successes[address], labels, self.get_timestamp(), self.internal)
            mdc += MetricData(self.name + '.status', int(self.working[address]), self.labels, self.get_timestamp(), self.internal)

        return mdc