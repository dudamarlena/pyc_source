# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\gvizlib\chart.py
# Compiled at: 2020-01-22 21:37:50
# Size of source mod 2**32: 5873 bytes
"""
chart.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""
from .base import Base
import numpy as np, pandas as pd, string, sys

class Chart(Base):
    __doc__ = '\n    Generate the HTML for charts with Google Visualization API\n    '

    def __init__(self, kind='line'):
        """
        Initialize instance of Chart class

        Parameters
        ----------
        kind : str
            Kind of chart to create (e.g., line, ...)
        """
        self.kind = kind
        self._id = _generate_id()
        self._data = pd.DataFrame({'x': []})
        self._labels = []
        self._colors = []
        self._styles = []
        self._x_title = None
        self._y_title = None
        self._legend = None

    def legend(self, position='bottom'):
        self._legend = position

    def plot(self, x, y, label=None, color=None, style=None):
        if label is None:
            label = 'y' + str(len(self._data.columns) - 1)
        _data = pd.DataFrame({'x': x, label: y})
        self._data = self._data.merge(_data, how='outer', on='x').fillna(0)
        self._labels.append(label)
        self._colors.append(color)
        self._styles.append(style)

    def show(self, render_loader=True, width='100%', height='500px'):
        output = '' if not render_loader else '\n            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n        '
        output += '\n            <script type="text/javascript">\n        '
        output += '\n            google.charts.load("current", {{packages: ["corechart", "{kind}"]}});\n            google.charts.setOnLoadCallback(drawChart_{id});\n            function drawChart_{id}() {{\n        '.format(kind=(self.kind), id=(self._id))
        output += '\n            var data = google.visualization.arrayToDataTable({data});\n            var options = {{\n        '.format(data=(repr(np.vstack([self._data.columns, self._data.values]).tolist())))
        output += '\n            hAxis: {{title: "{x_title}"}},\n        '.format(x_title=(self._x_title if self._x_title is not None else ''))
        output += '\n            vAxis: {{title: "{y_title}"}},\n        '.format(y_title=(self._y_title if self._y_title is not None else ''))
        output += '\n            legend: {{position: "{legend}"}},\n        '.format(legend=(self._legend if self._legend is not None else 'none'))
        output += '\n            }};\n            var chart = new google.visualization.LineChart(document.getElementById("{id}"));\n            chart.draw(data, options);\n            }}\n            </script>\n            <div id="{id}" style="width: {width}; height: {height};"></div>\n        '.format(id=(self._id), width=width, height=height)
        return output

    def xtitle(self, title):
        self._x_title = title

    def ytitle(self, title):
        self._y_title = title


class GoogleTable:

    def __init__(self, data, row_numbers=True):
        self._data = data
        self._id = _generate_id()
        self.row_numbers = row_numbers

    def show(self, render_loader=True):
        output = '' if not render_loader else '\n            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n        '
        output += '\n            <script type="text/javascript">\n        '
        output += '\n            google.charts.load("current", {{packages: ["table"]}});\n            google.charts.setOnLoadCallback(drawTable_{id});\n            function drawTable_{id}() {{\n        '.format(id=(self._id))
        _data = self._data.reset_index().fillna(0)
        output += '\n            var data = google.visualization.arrayToDataTable({data});\n            var options = {{\n        '.format(data=(repr(np.vstack([_data.columns, _data.values]).tolist())))
        output += '\n            showRowNumber: {row_numbers},\n            width: "100%",\n        '.format(row_numbers=('true' if self.row_numbers else 'false'))
        output += '\n            }};\n            var table = new google.visualization.Table(document.getElementById("{id}"));\n            table.draw(data, options);\n            }}\n            </script>\n            <div id="{id}"></div>\n        '.format(id=(self._id))
        return output


def _generate_id(n=10):
    while 1:
        _id = ''.join(np.random.choice(list(string.ascii_lowercase), n))
        if _id not in this.cache:
            break

    this.cache.append(_id)
    return _id