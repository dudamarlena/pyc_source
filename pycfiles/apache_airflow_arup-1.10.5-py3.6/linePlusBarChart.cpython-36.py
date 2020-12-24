# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/linePlusBarChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5891 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class linePlusBarChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A linePlusBarChart Chart is a type of chart which displays information\n    as a series of data points connected by straight line segments\n    and with some series with rectangular bars with lengths proportional\n    to the values that they represent.\n\n    Python example::\n\n        from nvd3 import linePlusBarChart\n        chart = linePlusBarChart(name="linePlusBarChart",\n                             width=500, height=400, x_axis_format="%d %b %Y",\n                             x_is_date=True, focus_enable=True,\n                             yaxis2_format="function(d) { return d3.format(\',0.3f\')(d) }")\n\n        xdata = [1338501600000, 1345501600000, 1353501600000]\n        ydata = [6, 5, 1]\n        y2data = [0.002, 0.003, 0.004]\n\n        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},\n                       "date_format": "%d %b %Y %H:%S" }\n        chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie,\n                        bar=True)\n\n        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " min"}}\n        chart.add_serie(name="Serie 2", y=y2data, x=xdata, extra=extra_serie)\n        chart.buildcontent()\n\n    Note that in case you have two data serie with extreme different numbers,\n    that you would like to format in different ways,\n    you can pass a keyword *yaxis1_format* or *yaxis2_format* when\n    creating the graph.\n\n    In the example above the graph created presents the values of the second\n    data series with three digits right  of the decimal point.\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="linePlusBarChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n            data_linePlusBarChart=[{"bar": "true", "values": [{"y": 6, "x": 1338501600000}, {"y": 5, "x": 1345501600000}, {"y": 1, "x": 1353501600000}], "key": "Serie 1", "yAxis": "1"}, {"values": [{"y": 0.002, "x": 1338501600000}, {"y": 0.003, "x": 1345501600000}, {"y": 0.004, "x": 1353501600000}], "key": "Serie 2", "yAxis": "1"}];\n            nv.addGraph(function() {\n                var chart = nv.models.linePlusBarChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_linePlusBarChart;\n\n                    chart.y2Axis\n                        .tickFormat(function(d) { return d3.format(\',0.3f\')(d) });\n                    chart.xAxis\n                        .tickFormat(function(d) { return d3.time.format(\'%d %b %Y\')(new Date(parseInt(d))) });\n                    chart.y1Axis\n                        .tickFormat(function(d) { return d3.format(\',f\')(d) });\n\n                    chart.tooltipContent(function(key, y, e, graph) {\n                        var x = d3.time.format("%d %b %Y %H:%S")(new Date(parseInt(graph.point.x)));\n                        var y = String(graph.point.y);\n                        if(key.indexOf(\'Serie 1\') > -1 ){\n                                var y = \'There are \' +  String(graph.point.y)  + \' calls\';\n                            }\n                            if(key.indexOf(\'Serie 2\') > -1 ){\n                                var y = \'There are \' +  String(graph.point.y)  + \' min\';\n                            }\n                        tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' on \' + x;\n                        return tooltip_str;\n                    });\n                    chart.showLegend(true);\n                d3.select(\'#linePlusBarChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'width\', 500)\n                    .attr(\'height\', 400)\n                    .call(chart);\n            });\n        </script>\n\n    '
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