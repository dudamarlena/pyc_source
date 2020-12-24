# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/multiBarHorizontalChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3680 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class multiBarHorizontalChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A multiple horizontal bar graph contains comparisons of two or more categories or bars.\n\n    Python example::\n\n        from nvd3 import multiBarHorizontalChart\n        chart = multiBarHorizontalChart(name=\'multiBarHorizontalChart\', height=400, width=400)\n        xdata = [-14, -7, 7, 14]\n        ydata = [-6, 5, -1, 9]\n        y2data = [-23, -6, -32, 9]\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " balls"}}\n        chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie)\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " calls"}}\n        chart.add_serie(name="Serie 2", y=y2data, x=xdata, extra=extra_serie)\n        chart.buildcontent()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="multiBarHorizontalChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n\n            data_multiBarHorizontalChart=[{"values":\n                [{"y": -6, "x": -14}, {"y": 5, "x": -7}, {"y": -1, "x": 7}, {"y": 9, "x": 14}],\n                "key": "Serie 1", "yAxis": "1"},\n                {"values":\n                    [{"y": -23, "x": -14}, {"y": -6, "x": -7}, {"y": -32, "x": 7}, {"y": 9, "x": 14}],\n                "key": "Serie 2", "yAxis": "1"}];\n\n            nv.addGraph(function() {\n                var chart = nv.models.multiBarHorizontalChart();\n\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n\n                var datum = data_multiBarHorizontalChart;\n\n                        chart.xAxis\n                            .tickFormat(d3.format(\',.2f\'));\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.2f\'));\n\n                        chart.tooltipContent(function(key, y, e, graph) {\n                            var x = String(graph.point.x);\n                            var y = String(graph.point.y);\n                                                if(key == \'Serie 1\'){\n                                var y =  String(graph.point.y)  + \' balls\';\n                            }\n                            if(key == \'Serie 2\'){\n                                var y =  String(graph.point.y)  + \' calls\';\n                            }\n\n                            tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' at \' + x;\n                            return tooltip_str;\n                        });\n\n                    chart.showLegend(true);\n\n                d3.select(\'#multiBarHorizontalChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'width\', 400)\n                    .attr(\'height\', 400)\n                    .call(chart);\n            });\n        </script>\n\n    '
    CHART_FILENAME = './multibarcharthorizontal.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(multiBarHorizontalChart, self).__init__)(**kwargs)
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '.2f')))
        self.create_y_axis('yAxis', format=(kwargs.get('y_axis_format', '.2f')))
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)