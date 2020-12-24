# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/entity/metric.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1337 bytes
from enum import Enum

class MetricType(Enum):
    LOSS = 'LOSS'


class Metric(object):

    def __init__(self, key, value: float, timestamp: float=None):
        self.key = key
        self.value = value
        self.timestamp = timestamp


class MetricMeta(object):

    def __init__(self, name: str, metric_type: MetricType, extra_metas: dict=None):
        self.name = name
        self.metric_type = metric_type
        self.metas = {}
        if extra_metas:
            self.metas.update(extra_metas)
        self.metas['name'] = name
        self.metas['metric_type'] = metric_type

    def update_metas(self, metas: dict):
        self.metas.update(metas)

    def to_dict(self):
        return self.metas