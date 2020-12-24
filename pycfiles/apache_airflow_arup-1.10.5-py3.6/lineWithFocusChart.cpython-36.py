# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/lineWithFocusChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4582 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class lineWithFocusChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A lineWithFocusChart or line graph is a type of chart which displays information\n    as a series of data points connected by straight line segments.\n    The lineWithFocusChart provide a smaller chart that act as a selector,\n    this is very useful if you want to zoom on a specific time period.\n\n    Python example::\n\n        from nvd3 import lineWithFocusChart\n        chart = lineWithFocusChart(name=\'lineWithFocusChart\', x_is_date=True, x_axis_format="%d %b %Y")\n        xdata = [1365026400000000, 1365026500000000, 1365026600000000, 1365026700000000, 1365026800000000, 1365026900000000, 1365027000000000]\n        ydata = [-6, 5, -1, 2, 4, 8, 10]\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " ext"},\n                       "date_format": "%d %b %Y"}\n        chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="lineWithFocusChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n            data_lineWithFocusChart=[{"values": [{"y": -6, "x": 1365026400000000}, {"y": 5, "x": 1365026500000000}, {"y": -1, "x": 1365026600000000}], "key": "Serie 1", "yAxis": "1"}];\n            nv.addGraph(function() {\n                var chart = nv.models.lineWithFocusChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_lineWithFocusChart;\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.2f\'));\n                        chart.y2Axis\n                            .tickFormat(d3.format(\',.2f\'));\n                        chart.xAxis\n                            .tickFormat(function(d) { return d3.time.format(\'%d %b %Y\')(new Date(parseInt(d))) });\n                        chart.x2Axis\n                            .tickFormat(function(d) { return d3.time.format(\'%d %b %Y\')(new Date(parseInt(d))) });\n\n                    chart.tooltipContent(function(key, y, e, graph) {\n                        var x = d3.time.format("%d %b %Y")(new Date(parseInt(graph.point.x)));\n                        var y = String(graph.point.y);\n                                            if(key == \'Serie 1\'){\n                                var y =  String(graph.point.y)  + \' ext\';\n                            }\n\n                        tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' on \' + x;\n                        return tooltip_str; });\n\n                    chart.showLegend(true);\n\n                d3.select(\'#lineWithFocusChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'height\', 450)\n                    .call(chart); });\n        </script>\n\n    '
    CHART_FILENAME = './linewfocuschart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(lineWithFocusChart, self).__init__)(**kwargs)
        self.model = 'lineWithFocusChart'
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
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
        self.create_y_axis('yAxis', format=(kwargs.get('y_axis_format', '.2f')))
        self.create_y_axis('y2Axis', format=(kwargs.get('y_axis_format', '.2f')))
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)