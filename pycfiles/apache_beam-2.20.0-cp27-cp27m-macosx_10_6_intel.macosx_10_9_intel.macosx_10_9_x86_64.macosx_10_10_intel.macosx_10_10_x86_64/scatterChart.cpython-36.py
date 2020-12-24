# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/scatterChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4590 bytes
__doc__ = '\nPython-nvd3 is a Python wrapper for NVD3 graph library.\nNVD3 is an attempt to build re-usable charts and chart components\nfor d3.js without taking away the power that d3.js gives you.\n\nProject location : https://github.com/areski/python-nvd3\n'
from .NVD3Chart import NVD3Chart, TemplateMixin

class scatterChart(TemplateMixin, NVD3Chart):
    """scatterChart"""
    CHART_FILENAME = './scatterchart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(scatterChart, self).__init__)(**kwargs)
        self.model = 'scatterChart'
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '.02f')), label=(kwargs.get('x_axis_label', None)))
        self.create_y_axis('yAxis', format=(kwargs.get('y_axis_format', '.02f')), label=(kwargs.get('y_axis_label', None)))
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)