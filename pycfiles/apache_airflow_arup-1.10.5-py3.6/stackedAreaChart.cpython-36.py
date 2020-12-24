# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/stackedAreaChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4142 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class stackedAreaChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    The stacked area chart is identical to the area chart, except the areas are stacked\n    on top of each other, rather than overlapping. This can make the chart much easier to read.\n\n    Python example::\n\n        from nvd3 import stackedAreaChart\n        chart = stackedAreaChart(name=\'stackedAreaChart\', height=400, width=400)\n\n        xdata = [100, 101, 102, 103, 104, 105, 106,]\n        ydata = [6, 11, 12, 7, 11, 10, 11]\n        ydata2 = [8, 20, 16, 12, 20, 28, 28]\n\n        extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " min"}}\n        chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie)\n        chart.add_serie(name="Serie 2", y=ydata2, x=xdata, extra=extra_serie)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="stackedAreaChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n\n\n            data_stackedAreaChart=[{"values": [{"y": 6, "x": 100}, {"y": 11, "x": 101}, {"y": 12, "x": 102}, {"y": 7, "x": 103}, {"y": 11, "x": 104}, {"y": 10, "x": 105}, {"y": 11, "x": 106}], "key": "Serie 1", "yAxis": "1"}, {"values": [{"y": 8, "x": 100}, {"y": 20, "x": 101}, {"y": 16, "x": 102}, {"y": 12, "x": 103}, {"y": 20, "x": 104}, {"y": 28, "x": 105}, {"y": 28, "x": 106}], "key": "Serie 2", "yAxis": "1"}];\n            nv.addGraph(function() {\n                var chart = nv.models.stackedAreaChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_stackedAreaChart;\n                        chart.xAxis\n                            .tickFormat(d3.format(\',.2f\'));\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.2f\'));\n\n                        chart.tooltipContent(function(key, y, e, graph) {\n                            var x = String(graph.point.x);\n                            var y = String(graph.point.y);\n                                                if(key == \'Serie 1\'){\n                                var y = \'There is \' +  String(graph.point.y)  + \' min\';\n                            }\n                            if(key == \'Serie 2\'){\n                                var y = \'There is \' +  String(graph.point.y)  + \' min\';\n                            }\n\n                            tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' at \' + x;\n                            return tooltip_str;\n                        });\n                    chart.showLegend(true);\n                d3.select(\'#stackedAreaChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'width\', 400)\n                    .attr(\'height\', 400)\n                    .call(chart);\n            });\n        </script>\n\n    '
    CHART_FILENAME = './stackedareachart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(stackedAreaChart, self).__init__)(**kwargs)
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        self.model = 'stackedAreaChart'
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