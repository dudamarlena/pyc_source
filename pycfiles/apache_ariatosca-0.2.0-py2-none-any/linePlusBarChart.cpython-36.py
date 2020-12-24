# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/linePlusBarChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5891 bytes
__doc__ = '\nPython-nvd3 is a Python wrapper for NVD3 graph library.\nNVD3 is an attempt to build re-usable charts and chart components\nfor d3.js without taking away the power that d3.js gives you.\n\nProject location : https://github.com/areski/python-nvd3\n'
from .NVD3Chart import NVD3Chart, TemplateMixin

class linePlusBarChart(TemplateMixin, NVD3Chart):
    """linePlusBarChart"""
    CHART_FILENAME = './lineplusbarchart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(linePlusBarChart, self).__init__)(**kwargs)
        self.model = 'linePlusBarChart'
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        self.yaxis1_format = kwargs.get('yaxis1_format', "function(d) { return d3.format(',f')(d) }")
        self.yaxis2_format = kwargs.get('yaxis2_format', "function(d) { return d3.format(',f')(d) }")
        if kwargs.get('x_is_date', False):
            self.set_date_flag(True)
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '%d %b %Y %H %S')),
              date=True)
            self.create_x_axis('x2Axis', format=(kwargs.get('x_axis_format', '%d %b %Y %H %S')),
              date=True)
            self.set_custom_tooltip_flag(True)
        else:
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '.2f')))
            self.create_x_axis('x2Axis', format=(kwargs.get('x_axis_format', '.2f')))
        self.create_y_axis('y1Axis', format=(self.yaxis1_format), custom_format=True)
        self.create_y_axis('y2Axis', format=(self.yaxis2_format), custom_format=True)
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)