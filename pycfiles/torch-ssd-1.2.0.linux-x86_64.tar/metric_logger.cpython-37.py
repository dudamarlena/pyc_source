# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/utils/metric_logger.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 1803 bytes
from collections import deque, defaultdict
import numpy as np, torch

class SmoothedValue:
    __doc__ = 'Track a series of values and provide access to smoothed values over a\n    window or the global series average.\n    '

    def __init__(self, window_size=10):
        self.deque = deque(maxlen=window_size)
        self.value = np.nan
        self.series = []
        self.total = 0.0
        self.count = 0

    def update(self, value):
        self.deque.append(value)
        self.series.append(value)
        self.count += 1
        self.total += value
        self.value = value

    @property
    def median(self):
        values = np.array(self.deque)
        return np.median(values)

    @property
    def avg(self):
        values = np.array(self.deque)
        return np.mean(values)

    @property
    def global_avg(self):
        return self.total / self.count


class MetricLogger:

    def __init__(self, delimiter=', '):
        self.meters = defaultdict(SmoothedValue)
        self.delimiter = delimiter

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, torch.Tensor):
                v = v.item()
            assert isinstance(v, (float, int))
            self.meters[k].update(v)

    def __getattr__(self, attr):
        if attr in self.meters:
            return self.meters[attr]
        if attr in self.__dict__:
            return self.__dict__[attr]
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, attr))

    def __str__(self):
        loss_str = []
        for name, meter in self.meters.items():
            loss_str.append('{}: {:.3f} ({:.3f})'.format(name, meter.avg, meter.global_avg))

        return self.delimiter.join(loss_str)