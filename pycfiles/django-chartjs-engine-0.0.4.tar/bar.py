# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jeff/Development/python/chartjs_engine/chartjs_engine/views/bar.py
# Compiled at: 2016-12-29 17:37:41
"""
The bar chart class
"""
from .base import Chart
from django.template.loader import render_to_string
import json

class BarChart(Chart):
    """
        Making the JSON data necessary for a bar chart
        DOCS: http://www.chartjs.org/docs/#bar-chart-introduction
        """

    def get_options(self):
        """Gets the options for the chart"""
        self.options = {'scales': {'yAxes': [
                              {'ticks': {'beginAtZero': True}}]}}
        return self.options

    def get_data(self):
        """Populating self.data with self.datasets"""
        self.data['datasets'] = []
        for i, name in enumerate(self.datasets):
            if len(self.datasets) == 1:
                self.colors = [ self.random_color() for d in self.datasets[name] ]
            else:
                self.rand_color = self.random_color()
                self.colors = [ self.rand_color for d in self.datasets[name] ]
            self.data['datasets'].append({'label': name, 
               'backgroundColor': [ color[0] for color in self.colors ], 'borderColor': [ color[1] for color in self.colors ], 'borderWidth': 3, 
               'data': self.datasets[name]})

        return self.data

    def make_context(self):
        """Making the context to be returned to the render functions"""
        self.context = {'chart_type': self.chart_type, 
           'chart_name': self.chart_name, 
           'data': json.dumps(self.data), 
           'options': json.dumps(self.options)}
        return self.context

    def to_string(self):
        """Rendering bar chart data to a template, returning string"""
        self.get_options()
        self.get_data()
        self.make_context()
        return render_to_string('chartjs_engine/chart.html', self.context)