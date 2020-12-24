# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ben/Documents/Projects/C3PyO/c3pyo/bar_chart.py
# Compiled at: 2016-10-20 16:42:44
# Size of source mod 2**32: 1547 bytes
import json
from .base import C3Chart
from c3pyo.utils import is_iterable

class BarChart(C3Chart):

    def __init__(self, **kwargs):
        super(BarChart, self).__init__(**kwargs)
        self.bar_ratio = kwargs.get('bar_ratio', 0.8)
        self.data = []
        self.chart_type = 'bar'

    def set_data(self, data):
        if is_iterable(data):
            for i in data:
                self.data.append([i])

        else:
            if isinstance(data, dict):
                keys = sorted([key for key in data])
                for key in keys:
                    self.data.append([key, data[key]])

            else:
                raise TypeError('x_data must be iterable or of type dict')

    def get_data_for_json(self):
        return {'columns': self.data, 
         'type': self.chart_type}

    def get_axis_for_json(self):
        return {'x': {'type': 'category', 
               'categories': [self.x_label], 
               'label': self.x_label}, 
         
         'y': {'label': self.y_label}}

    def get_chart_json(self):
        chart_json = {'bindto': self.chart_div, 
         'data': self.get_data_for_json(), 
         'legend': self.get_legend_for_json(), 
         'grid': self.get_grid_for_json(), 
         'axis': self.get_axis_for_json()}
        chart_json = json.dumps(chart_json)
        return chart_json

    def plot(self):
        chart_json = self.get_chart_json()
        self.plot_graph(chart_json)