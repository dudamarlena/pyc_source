# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Documents/Projects/C3PyO/c3pyo/pie_chart.py
# Compiled at: 2016-10-20 16:42:35
# Size of source mod 2**32: 1086 bytes
import json, numbers
from .base import C3Chart
from c3pyo.utils import is_iterable

class PieChart(C3Chart):

    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.data = []
        self.chart_type = 'pie'

    def set_data(self, data):
        if isiterable(data):
            for idx, value in enumerate(data):
                if isinstance(value, numbers.Number):
                    self.data.append(['y{}'.format(idx + 1), value])
                else:
                    msg = 'Expected collection of numbers, received {}'
                    raise TypeError(msg.format(value))

        else:
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], numbers.Number):
                        self.data.append([key, data[key]])
                    else:
                        msg = 'Expected number, received {} of type {}'
                        raise TypeError(msg.format(data[key], type(key)))

            else:
                raise TypeError('x_data must be a collection or dict, received {}'.format(type(data)))