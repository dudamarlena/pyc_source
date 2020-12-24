# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c3pyo/pie_chart.py
# Compiled at: 2016-12-08 12:08:28
import numbers
from c3pyo import C3Chart

class PieChart(C3Chart):

    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self._data = []
        self._chart_type = 'pie'
        self.y_number = 1

    def plot(self, y, color=None, label=None):
        if not label:
            y_series_label = ('y{}').format(self.y_number)
        else:
            y_series_label = label
        if isinstance(y, numbers.Number):
            y_data = [
             y_series_label, y]
        else:
            y_data = [
             y_series_label]
            y_data.extend(y)
        if color:
            self.add_color(color, y_series_label)
        self._data.append(y_data)

    def get_data_for_json(self):
        return {'columns': self._data, 
           'type': self._chart_type, 
           'colors': self._colors}

    def get_axis_for_json(self):
        return {}


class DonutChart(PieChart):

    def __init__(self, **kwargs):
        super(DonutChart, self).__init__(**kwargs)
        self._chart_type = 'donut'
        self._donut_title_value = kwargs.get('donut_title', None)
        return

    def donut_title(self, title):
        self._donut_title_value = title

    def get_donut_for_json(self):
        if not self._donut_title_value:
            return
        else:
            return {'title': self._donut_title_value}
            return