# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/scatterChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4590 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class scatterChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A scatter plot or scattergraph is a type of mathematical diagram using Cartesian\n    coordinates to display values for two variables for a set of data.\n    The data is displayed as a collection of points, each having the value of one variable\n    determining the position on the horizontal axis and the value of the other variable\n    determining the position on the vertical axis.\n\n    Python example::\n\n        from nvd3 import scatterChart\n        chart = scatterChart(name=\'scatterChart\', height=400, width=400)\n        xdata = [3, 4, 0, -3, 5, 7]\n        ydata = [-1, 2, 3, 3, 15, 2]\n        ydata2 = [1, -2, 4, 7, -5, 3]\n\n        kwargs1 = {\'shape\': \'circle\', \'size\': \'1\'}\n        kwargs2 = {\'shape\': \'cross\', \'size\': \'10\'}\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " call"}}\n        chart.add_serie(name="series 1", y=ydata, x=xdata, extra=extra_serie, **kwargs1)\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " min"}}\n        chart.add_serie(name="series 2", y=ydata2, x=xdata, extra=extra_serie, **kwargs2)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="scatterChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n\n        data_scatterChart=[{"values": [{"y": -1, "x": 3, "shape": "circle",\n            "size": "1"}, {"y": 2, "x": 4, "shape": "circle", "size": "1"},\n            {"y": 3, "x": 0, "shape": "circle", "size": "1"},\n            {"y": 3, "x": -3, "shape": "circle", "size": "1"},\n            {"y": 15, "x": 5, "shape": "circle", "size": "1"},\n            {"y": 2, "x": 7, "shape": "circle", "size": "1"}],\n            "key": "series 1", "yAxis": "1"},\n            {"values": [{"y": 1, "x": 3, "shape": "cross", "size": "10"},\n            {"y": -2, "x": 4, "shape": "cross", "size": "10"},\n            {"y": 4, "x": 0, "shape": "cross", "size": "10"},\n            {"y": 7, "x": -3, "shape": "cross", "size": "10"},\n            {"y": -5, "x": 5, "shape": "cross", "size": "10"},\n            {"y": 3, "x": 7, "shape": "cross", "size": "10"}],\n            "key": "series 2", "yAxis": "1"}];\n        nv.addGraph(function() {\n        var chart = nv.models.scatterChart();\n\n        chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n\n        var datum = data_scatterChart;\n\n                chart.xAxis\n                    .tickFormat(d3.format(\',.02f\'));\n                chart.yAxis\n                    .tickFormat(d3.format(\',.02f\'));\n\n                chart.tooltipContent(function(key, y, e, graph) {\n                    var x = String(graph.point.x);\n                    var y = String(graph.point.y);\n                                        if(key == \'series 1\'){\n                        var y =  String(graph.point.y)  + \' call\';\n                    }\n                    if(key == \'series 2\'){\n                        var y =  String(graph.point.y)  + \' min\';\n                    }\n\n                    tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' at \' + x;\n                    return tooltip_str;\n                });\n\n        chart.showLegend(true);\n\n        chart\n        .showDistX(true)\n        .showDistY(true)\n        .color(d3.scale.category10().range());\n\n            d3.select(\'#scatterChart svg\')\n                .datum(datum)\n                .transition().duration(500)\n                .attr(\'width\', 400)\n                .attr(\'height\', 400)\n                .call(chart);\n        });\n        </script>\n\n    '
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