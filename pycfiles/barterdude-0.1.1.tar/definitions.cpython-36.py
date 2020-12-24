# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/olxbr/BarterDude/barterdude/hooks/metrics/prometheus/definitions.py
# Compiled at: 2020-04-30 17:51:17
# Size of source mod 2**32: 3582 bytes
from copy import copy
from prometheus_client import CollectorRegistry, Counter, Histogram
from typing import Iterable
from barterdude.hooks.metrics.prometheus.metrics import Metrics

class Definitions:
    MESSAGE_UNITS = 'messages'
    ERROR_UNITS = 'errors'
    TIME_UNITS = 'seconds'
    NAMESPACE = 'barterdude'
    BEFORE_CONSUME = 'before_consume'
    SUCCESS = 'success'
    FAIL = 'fail'
    TIME_MEASURE = 'time_measure'
    CONNECTION_FAIL = 'connection_fail'

    def __init__(self, registry: CollectorRegistry, metrics: Metrics, labelkeys: Iterable[str], time_buckets: tuple=Histogram.DEFAULT_BUCKETS):
        self._Definitions__registry = registry
        self._Definitions__labelkeys = labelkeys
        self._Definitions__time_buckets = time_buckets
        self._Definitions__metrics = metrics

    def save_metrics(self):
        self._prepare_before_consume((self.BEFORE_CONSUME),
          namespace=(self.NAMESPACE),
          unit=(self.MESSAGE_UNITS))
        self._prepare_on_complete((self.SUCCESS),
          namespace=(self.NAMESPACE),
          unit=(self.MESSAGE_UNITS))
        self._prepare_on_complete((self.FAIL),
          namespace=(self.NAMESPACE),
          unit=(self.MESSAGE_UNITS))
        self._prepare_time_measure((self.TIME_MEASURE),
          namespace=(self.NAMESPACE),
          unit=(self.TIME_UNITS))
        self._prepare_on_connection_fail((self.CONNECTION_FAIL),
          namespace=(self.NAMESPACE),
          unit=(self.ERROR_UNITS))

    def _prepare_before_consume(self, name: str, namespace: str='', unit: str=''):
        self._Definitions__metrics[name] = Counter(name='received_number_before_consume',
          documentation='Messages that worker received from queue(s)',
          labelnames=(copy(self._Definitions__labelkeys)),
          namespace=namespace,
          unit=unit,
          registry=(self._Definitions__registry))

    def _prepare_on_complete(self, state: str, namespace: str='', unit: str=''):
        self._Definitions__metrics[state] = Counter(name=f"consumed_number_on_{state}",
          documentation=f"Messages that worker consumed with {state} from queue(s)",
          labelnames=(self._Definitions__labelkeys + ['state', 'error']),
          namespace=namespace,
          unit=unit,
          registry=(self._Definitions__registry))

    def _prepare_time_measure(self, name: str, namespace: str='', unit: str=''):
        self._Definitions__metrics[name] = Histogram(name='time_spent_processing_message',
          documentation='Time spent when function was processing a message',
          buckets=(self._Definitions__time_buckets),
          labelnames=(self._Definitions__labelkeys + ['state', 'error']),
          namespace=namespace,
          unit=unit,
          registry=(self._Definitions__registry))

    def _prepare_on_connection_fail(self, state: str, namespace: str, unit: str):
        self._Definitions__metrics[state] = Counter(name='connection_fail',
          documentation='Number of times barterdude failed to connect to the AMQP broker',
          labelnames=(self._Definitions__labelkeys),
          namespace=namespace,
          unit=unit,
          registry=(self._Definitions__registry))