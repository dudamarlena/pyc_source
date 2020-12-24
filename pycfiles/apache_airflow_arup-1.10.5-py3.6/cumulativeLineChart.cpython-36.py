# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/cumulativeLineChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4073 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class cumulativeLineChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A cumulative line chart is used when you have one important grouping representing\n    an ordered set of data and one value to show, summed over time.\n\n    Python example::\n\n        from nvd3 import cumulativeLineChart\n        chart = cumulativeLineChart(name=\'cumulativeLineChart\', x_is_date=True)\n        xdata = [1365026400000000, 1365026500000000, 1365026600000000]\n        ydata = [6, 5, 1]\n        y2data = [36, 55, 11]\n\n        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}\n        chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie)\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " mins"}}\n        chart.add_serie(name="Serie 2", y=y2data, x=xdata, extra=extra_serie)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="cumulativeLineChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n            data_cumulativeLineChart=[{"values": [{"y": 6, "x": 1365026400000000},\n            {"y": 5, "x": 1365026500000000},\n            {"y": 1, "x": 1365026600000000}],\n            "key": "Serie 1", "yAxis": "1"},\n            {"values": [{"y": 36, "x": 1365026400000000},\n            {"y": 55, "x": 1365026500000000},\n            {"y": 11, "x": 1365026600000000}], "key": "Serie 2", "yAxis": "1"}];\n            nv.addGraph(function() {\n                var chart = nv.models.cumulativeLineChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_cumulativeLineChart;\n\n                        chart.xAxis\n                            .tickFormat(function(d) { return d3.time.format(\'%d %b %Y\')(new Date(parseInt(d))) });\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.1%\'));\n\n                    chart.tooltipContent(function(key, y, e, graph) {\n                        var x = d3.time.format("%d %b %Y")(new Date(parseInt(graph.point.x)));\n                        var y = String(graph.point.y);\n                        if(key == \'Serie 1\'){\n                                var y = \'There are \' +  String(e)  + \' calls\';\n                            }if(key == \'Serie 2\'){\n                                var y =  String(e)  + \' mins\';\n                            }\n                        tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' on \' + x;\n                        return tooltip_str;\n                    });\n                    chart.showLegend(true);\n\n                d3.select(\'#cumulativeLineChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'height\', 450)\n                    .call(chart); });\n        </script>\n\n    '
    CHART_FILENAME = './cumulativelinechart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(cumulativeLineChart, self).__init__)(**kwargs)
        self.model = 'cumulativeLineChart'
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        if kwargs.get('x_is_date', False):
            self.set_date_flag(True)
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '%d %b %Y')),
              date=True)
            self.set_custom_tooltip_flag(True)
        else:
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '.2f')))
        self.create_y_axis('yAxis', format=(kwargs.get('y_axis_format', '.1%')))
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)