# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/multiBarChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3433 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class multiBarChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A multiple bar graph contains comparisons of two or more categories or bars.\n    One axis represents a quantity and the other axis identifies a specific feature\n    about the categories. Reading a multiple bar graph includes looking at extremes\n    (tallest/longest vs. shortest) in each grouping.\n\n    Python example::\n\n        from nvd3 import multiBarChart\n        chart = multiBarChart(width=500, height=400, x_axis_format=None)\n        xdata = [\'one\', \'two\', \'three\', \'four\']\n        ydata1 = [6, 12, 9, 16]\n        ydata2 = [8, 14, 7, 11]\n\n        chart.add_serie(name="Serie 1", y=ydata1, x=xdata)\n        chart.add_serie(name="Serie 2", y=ydata2, x=xdata)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="multiBarChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n\n            data_multiBarChart=[{"values":\n                                [{"y": 6, "x": "one"},\n                                {"y": 12, "x": "two"},\n                                {"y": 9, "x": "three"},\n                                {"y": 16, "x": "four"}],\n                                "key": "Serie 1", "yAxis": "1"},\n                                {"values":\n                                    [{"y": 8, "x": "one"},\n                                    {"y": 14, "x": "two"},\n                                    {"y": 7, "x": "three"},\n                                    {"y": 11, "x": "four"}],\n                                "key": "Serie 2", "yAxis": "1"}];\n\n            nv.addGraph(function() {\n                var chart = nv.models.multiBarChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_multiBarChart;\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.2f\'));\n                    chart.showLegend(true);\n                d3.select(\'#multiBarChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'width\', 500)\n                    .attr(\'height\', 400)\n                    .call(chart);\n            });\n\n\n        </script>\n\n    '
    CHART_FILENAME = './multibarchart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(multiBarChart, self).__init__)(**kwargs)
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        if kwargs.get('x_is_date', False):
            self.set_date_flag(True)
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '%d %b %Y')),
              date=True)
            self.set_custom_tooltip_flag(True)
        else:
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '.2f')))
        self.create_y_axis('yAxis', format=(kwargs.get('y_axis_format', '.2f')))
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)