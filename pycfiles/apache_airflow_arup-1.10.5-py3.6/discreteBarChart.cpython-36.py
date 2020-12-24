# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/discreteBarChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3159 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class discreteBarChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A discrete bar chart or bar graph is a chart with rectangular bars with\n    lengths proportional to the values that they represent.\n\n    Python example::\n\n        from nvd3 import discreteBarChart\n        chart = discreteBarChart(name=\'discreteBarChart\', height=400, width=400)\n\n        xdata = ["A", "B", "C", "D", "E", "F"]\n        ydata = [3, 4, 0, -3, 5, 7]\n\n        chart.add_serie(y=ydata, x=xdata)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="discreteBarChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n            data_discreteBarChart=[{"values": [{"y": 3, "x": "A"}, {"y": 4, "x": "B"}, {"y": 0, "x": "C"}, {"y": -3, "x": "D"}, {"y": 5, "x": "E"}, {"y": 7, "x": "F"}], "key": "Serie 1", "yAxis": "1"}];\n\n            nv.addGraph(function() {\n                var chart = nv.models.discreteBarChart();\n\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n\n                var datum = data_discreteBarChart;\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.0f\'));\n                        chart.tooltipContent(function(key, y, e, graph) {\n                            var x = String(graph.point.x);\n                            var y = String(graph.point.y);\n                            var y = String(graph.point.y);\n\n                            tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' at \' + x;\n                            return tooltip_str;\n                        });\n\n                d3.select(\'#discreteBarChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'width\', 400)\n                    .attr(\'height\', 400)\n                    .call(chart);\n            });\n        </script>\n\n\n    '
    CHART_FILENAME = './discretebarchart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(discreteBarChart, self).__init__)(**kwargs)
        self.model = 'discreteBarChart'
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        if kwargs.get('x_is_date', False):
            self.set_date_flag(True)
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '%d %b %Y %H %S')),
              date=True)
        else:
            self.create_x_axis('xAxis', format=None)
        self.create_y_axis('yAxis', format=(kwargs.get('y_axis_format', '.0f')))
        self.set_custom_tooltip_flag(True)
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)