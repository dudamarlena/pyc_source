# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jeff/Development/python/chartjs_engine/chartjs_engine/views/engine.py
# Compiled at: 2016-12-29 05:29:36
"""
Charting engine which takes the input and routes it to the proper Chart sublcass.
"""
from .line import LineChart
from .bar import BarChart
from .pie_doughnut import PieDoughnutChart
from .base import Chart

class ChartEngine(object):
    """An engine to make all of the charts necessary"""

    def __init__(self, **kwargs):
        """take in chart options and decide what kind of chart to make"""
        charts = {'line': LineChart, 
           'bar': BarChart, 
           'pie': PieDoughnutChart, 
           'doughnut': PieDoughnutChart}
        self.chart = charts[kwargs['chart_type']](chart_name=kwargs['chart_name'], chart_type=kwargs['chart_type'], chart_labels=kwargs['chart_labels'], options=kwargs['options'], datasets=kwargs['datasets'])

    def make_chart(self):
        """Render the proper chart from the given"""
        return self.chart.to_string()