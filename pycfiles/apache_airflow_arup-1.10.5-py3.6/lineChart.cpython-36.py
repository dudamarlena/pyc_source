# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/lineChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5553 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class lineChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A line chart or line graph is a type of chart which displays information\n    as a series of data points connected by straight line segments.\n\n    Python example::\n\n        from nvd3 import lineChart\n        chart = lineChart(name="lineChart", x_is_date=False, x_axis_format="AM_PM")\n\n        xdata = range(24)\n        ydata = [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 4, 3, 3, 5, 7, 5, 3, 16, 6, 9, 15, 4, 12]\n        ydata2 = [9, 8, 11, 8, 3, 7, 10, 8, 6, 6, 9, 6, 5, 4, 3, 10, 0, 6, 3, 1, 0, 0, 0, 1]\n\n        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}\n        chart.add_serie(y=ydata, x=xdata, name=\'sine\', extra=extra_serie, **kwargs1)\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " min"}}\n        chart.add_serie(y=ydata2, x=xdata, name=\'cose\', extra=extra_serie, **kwargs2)\n        chart.buildhtml()\n\n    Javascript renderd to:\n\n    .. raw:: html\n\n        <div id="lineChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n\n            data_lineChart=[{"values": [{"y": 0, "x": 0}, {"y": 0, "x": 1}, {"y": 1, "x": 2}, {"y": 1, "x": 3}, {"y": 0, "x": 4}, {"y": 0, "x": 5}, {"y": 0, "x": 6}, {"y": 0, "x": 7}, {"y": 1, "x": 8}, {"y": 0, "x": 9}, {"y": 0, "x": 10}, {"y": 4, "x": 11}, {"y": 3, "x": 12}, {"y": 3, "x": 13}, {"y": 5, "x": 14}, {"y": 7, "x": 15}, {"y": 5, "x": 16}, {"y": 3, "x": 17}, {"y": 16, "x": 18}, {"y": 6, "x": 19}, {"y": 9, "x": 20}, {"y": 15, "x": 21}, {"y": 4, "x": 22}, {"y": 12, "x": 23}], "key": "sine", "yAxis": "1"}, {"values": [{"y": 9, "x": 0}, {"y": 8, "x": 1}, {"y": 11, "x": 2}, {"y": 8, "x": 3}, {"y": 3, "x": 4}, {"y": 7, "x": 5}, {"y": 10, "x": 6}, {"y": 8, "x": 7}, {"y": 6, "x": 8}, {"y": 6, "x": 9}, {"y": 9, "x": 10}, {"y": 6, "x": 11}, {"y": 5, "x": 12}, {"y": 4, "x": 13}, {"y": 3, "x": 14}, {"y": 10, "x": 15}, {"y": 0, "x": 16}, {"y": 6, "x": 17}, {"y": 3, "x": 18}, {"y": 1, "x": 19}, {"y": 0, "x": 20}, {"y": 0, "x": 21}, {"y": 0, "x": 22}, {"y": 1, "x": 23}], "key": "cose", "yAxis": "1"}];\n\n            nv.addGraph(function() {\n                var chart = nv.models.lineChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_lineChart;\n                        chart.xAxis\n                            .tickFormat(function(d) { return get_am_pm(parseInt(d)); });\n                        chart.yAxis\n                            .tickFormat(d3.format(\',.02f\'));\n\n                        chart.tooltipContent(function(key, y, e, graph) {\n                            var x = String(graph.point.x);\n                            var y = String(graph.point.y);\n                                                if(key == \'sine\'){\n                                var y = \'There is \' +  String(graph.point.y)  + \' calls\';\n                            }\n                            if(key == \'cose\'){\n                                var y =  String(graph.point.y)  + \' min\';\n                            }\n\n                            tooltip_str = \'<center><b>\'+key+\'</b></center>\' + y + \' at \' + x;\n                            return tooltip_str;\n                        });\n                    chart.showLegend(true);\n                        function get_am_pm(d){\n                    if (d > 12) {\n                        d = d - 12; return (String(d) + \'PM\');\n                    }\n                    else {\n                        return (String(d) + \'AM\');\n                    }\n                };\n\n                d3.select(\'#lineChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'height\', 200)\n                    .call(chart);\n            return chart;\n        });\n        </script>\n\n    See the source code of this page, to see the underlying javascript.\n    '
    CHART_FILENAME = './linechart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(lineChart, self).__init__)(**kwargs)
        self.model = 'lineChart'
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        if kwargs.get('x_is_date', False):
            self.set_date_flag(True)
            self.create_x_axis('xAxis', format=(kwargs.get('x_axis_format', '%d %b %Y')),
              date=True)
            self.set_custom_tooltip_flag(True)
        else:
            if kwargs.get('x_axis_format') == 'AM_PM':
                self.x_axis_format = format = 'AM_PM'
            else:
                format = kwargs.get('x_axis_format', 'r')
            self.create_x_axis('xAxis', format=format, custom_format=(kwargs.get('x_custom_format', False)))
        self.create_y_axis('yAxis',
          format=(kwargs.get('y_axis_format', '.02f')),
          custom_format=(kwargs.get('y_custom_format', False)))
        self.set_graph_height(height)
        if width:
            self.set_graph_width(width)