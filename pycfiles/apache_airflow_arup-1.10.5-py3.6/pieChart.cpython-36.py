# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/pieChart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3689 bytes
"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""
from .NVD3Chart import NVD3Chart, TemplateMixin

class pieChart(TemplateMixin, NVD3Chart):
    __doc__ = '\n    A pie chart (or a circle graph) is a circular chart divided into sectors,\n    illustrating numerical proportion. In chart, the arc length of each sector\n    is proportional to the quantity it represents.\n\n    Python example::\n\n        from nvd3 import pieChart\n        chart = pieChart(name=\'pieChart\', color_category=\'category20c\',\n                         height=400, width=400)\n\n        xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawbery",\n                 "Pineapple"]\n        ydata = [3, 4, 0, 1, 5, 7, 3]\n\n        extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}\n        chart.add_serie(y=ydata, x=xdata, extra=extra_serie)\n        chart.buildhtml()\n\n    Javascript generated:\n\n    .. raw:: html\n\n        <div id="pieChart"><svg style="height:450px; width:100%"></svg></div>\n        <script>\n\n\n            data_pieChart=[{"values": [{"value": 3, "label": "Orange"},\n                           {"value": 4, "label": "Banana"},\n                           {"value": 0, "label": "Pear"},\n                           {"value": 1, "label": "Kiwi"},\n                           {"value": 5, "label": "Apple"},\n                           {"value": 7, "label": "Strawberry"},\n                           {"value": 3, "label": "Pineapple"}],\n                           "key": "Serie 1"}];\n\n            nv.addGraph(function() {\n                var chart = nv.models.pieChart();\n                chart.margin({top: 30, right: 60, bottom: 20, left: 60});\n                var datum = data_pieChart[0].values;\n                        chart.tooltipContent(function(key, y, e, graph) {\n                            var x = String(key);\n                            var y =  String(y)  + \' cal\';\n\n                            tooltip_str = \'<center><b>\'+x+\'</b></center>\' + y;\n                            return tooltip_str;\n                        });\n                    chart.showLegend(true);\n                    chart.showLabels(true);\n                    chart.donut(false);\n                chart\n                    .x(function(d) { return d.label })\n                    .y(function(d) { return d.value });\n                chart.width(400);\n                chart.height(400);\n\n                d3.select(\'#pieChart svg\')\n                    .datum(datum)\n                    .transition().duration(500)\n                    .attr(\'width\', 400)\n                    .attr(\'height\', 400)\n                    .call(chart);  });\n        </script>\n\n    '
    CHART_FILENAME = './piechart.html'
    template_chart_nvd3 = NVD3Chart.template_environment.get_template(CHART_FILENAME)

    def __init__(self, **kwargs):
        (super(pieChart, self).__init__)(**kwargs)
        height = kwargs.get('height', 450)
        width = kwargs.get('width', None)
        self.donut = kwargs.get('donut', False)
        self.donutRatio = kwargs.get('donutRatio', 0.35)
        self.color_list = []
        self.create_x_axis('xAxis', format=None)
        self.create_y_axis('yAxis', format=None)
        if height:
            self.set_graph_height(height)
        if width:
            self.set_graph_width(width)
        self.donut = kwargs.get('donut', False)
        self.donutRatio = kwargs.get('donutRatio', 0.35)