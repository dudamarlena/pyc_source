# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/asciichart.py
# Compiled at: 2018-10-14 23:35:19
# Size of source mod 2**32: 9498 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes, int, str
import sys
from math import cos
from math import sin
from math import pi
from math import floor
from math import ceil

class AsciiChart(object):
    __doc__ = "Can be used to plot price and trade history\n\n        :param int height: Height of the plot\n        :param int width: Width of the plot\n        :param int offset: Offset between tick strings and y-axis (default is 3)\n        :param str placeholder: Defines how the numbers on the y-axes are formated (default is '{:8.2f} ')\n        :param str charset: sets the charset for plotting, uft8 or ascii (default: utf8)\n    "

    def __init__(self, height=None, width=None, offset=3, placeholder='{:8.2f} ', charset='utf8'):
        self.height = height
        self.width = width
        self.offset = offset
        self.placeholder = placeholder
        self.clear_data()
        if charset == 'ascii' or sys.version_info[0] < 3:
            self.char_set = {'first_axis_elem':'|', 
             'axis_elem':'|', 
             'axis_elem_with_graph':'|', 
             'curve_ar':'\\', 
             'curve_lb':'\\', 
             'curve_br':'/', 
             'curve_la':'/', 
             'curve_hl':'-', 
             'curve_vl':'|', 
             'curve_hl_dot':'-', 
             'curve_vl_dot':'|'}
        else:
            self.char_set = {'first_axis_elem':'┼', 
             'axis_elem':'┤', 
             'axis_elem_with_graph':'┼', 
             'curve_ar':'╰', 
             'curve_lb':'╮', 
             'curve_br':'╭', 
             'curve_la':'╯', 
             'curve_hl':'─', 
             'curve_vl':'│', 
             'curve_hl_dot':'┈', 
             'curve_vl_dot':'┊'}

    def clear_data(self):
        """Clears all data"""
        self.canvas = []
        self.minimum = None
        self.maximum = None
        self.n = None
        self.skip = 1

    def set_parameter(self, height=None, offset=None, placeholder=None):
        """Can be used to change parameter"""
        if height is not None:
            self.height = height
        else:
            if offset is not None:
                self.offset = offset
            if placeholder is not None:
                self.placeholder = placeholder
        self._calc_plot_parameter()

    def adapt_on_series(self, series):
        """Calculates the minimum, maximum and length from the given list

            :param list series: time series to plot

            .. testcode::

                from dpaycli.asciichart import AsciiChart
                chart = AsciiChart()
                series = [1, 2, 3, 7, 2, -4, -2]
                chart.adapt_on_series(series)
                chart.new_chart()
                chart.add_axis()
                chart.add_curve(series)
                print(str(chart))

        """
        self.minimum = min(series)
        self.maximum = max(series)
        self.n = len(series)
        self._calc_plot_parameter()

    def _calc_plot_parameter(self, minimum=None, maximum=None, n=None):
        """Calculates parameter from minimum, maximum and length
        """
        if minimum is not None:
            self.minimum = minimum
        elif maximum is not None:
            self.maximum = maximum
        else:
            if n is not None:
                self.n = n
            else:
                if self.n is None or self.maximum is None or self.minimum is None:
                    return
                else:
                    interval = abs(float(self.maximum) - float(self.minimum))
                    if interval == 0:
                        interval = 1
                    if self.height is None:
                        self.height = interval
                self.ratio = self.height / interval
                self.min2 = floor(float(self.minimum) * self.ratio)
                self.max2 = ceil(float(self.maximum) * self.ratio)
                if self.min2 == self.max2:
                    self.max2 += 1
            intmin2 = int(self.min2)
            intmax2 = int(self.max2)
            self.rows = abs(intmax2 - intmin2)
            if self.width is not None:
                self.skip = int(self.n / self.width)
                if self.skip < 1:
                    self.skip = 1
            else:
                self.skip = 1

    def plot(self, series, return_str=False):
        """All in one function for plotting

            .. testcode::

                from dpaycli.asciichart import AsciiChart
                chart = AsciiChart()
                series = [1, 2, 3, 7, 2, -4, -2]
                chart.plot(series)
        """
        self.clear_data()
        self.adapt_on_series(series)
        self.new_chart()
        self.add_axis()
        self.add_curve(series)
        if not return_str:
            print(str(self))
        else:
            return str(self)

    def new_chart(self, minimum=None, maximum=None, n=None):
        """Clears the canvas

            .. testcode::

                from dpaycli.asciichart import AsciiChart
                chart = AsciiChart()
                series = [1, 2, 3, 7, 2, -4, -2]
                chart.adapt_on_series(series)
                chart.new_chart()
                chart.add_axis()
                chart.add_curve(series)
                print(str(chart))

        """
        if minimum is not None:
            self.minimum = minimum
        else:
            if maximum is not None:
                self.maximum = maximum
            if n is not None:
                self.n = n
        self._calc_plot_parameter()
        self.canvas = [[' '] * (int(self.n / self.skip) + self.offset) for i in range(self.rows + 1)]

    def add_axis(self):
        """Adds a y-axis to the canvas

            .. testcode::

                from dpaycli.asciichart import AsciiChart
                chart = AsciiChart()
                series = [1, 2, 3, 7, 2, -4, -2]
                chart.adapt_on_series(series)
                chart.new_chart()
                chart.add_axis()
                chart.add_curve(series)
                print(str(chart))

        """
        interval = abs(float(self.maximum) - float(self.minimum))
        intmin2 = int(self.min2)
        intmax2 = int(self.max2)
        for y in range(intmin2, intmax2 + 1):
            label = self.placeholder.format(float(self.maximum) - (y - intmin2) * interval / self.rows)
            if label:
                self._set_y_axis_elem(y, label)

    def _set_y_axis_elem(self, y, label):
        intmin2 = int(self.min2)
        self.canvas[(y - intmin2)][max(self.offset - len(label), 0)] = label
        if y == 0:
            self.canvas[(y - intmin2)][self.offset - 1] = self.char_set['first_axis_elem']
        else:
            self.canvas[(y - intmin2)][self.offset - 1] = self.char_set['axis_elem']

    def _map_y(self, y_float):
        intmin2 = int(self.min2)
        return int(round(y_float * self.ratio) - intmin2)

    def add_curve(self, series):
        """Add a curve to the canvas

            :param list series: List width float data points

            .. testcode::

                from dpaycli.asciichart import AsciiChart
                chart = AsciiChart()
                series = [1, 2, 3, 7, 2, -4, -2]
                chart.adapt_on_series(series)
                chart.new_chart()
                chart.add_axis()
                chart.add_curve(series)
                print(str(chart))

        """
        if self.n is None:
            self.adapt_on_series(series)
        if len(self.canvas) == 0:
            self.new_chart()
        y0 = self._map_y(series[0])
        self._set_elem(y0, -1, self.char_set['axis_elem_with_graph'])
        for x in range(0, len(series[::self.skip]) - 1):
            y0 = self._map_y(series[::self.skip][(x + 0)])
            y1 = self._map_y(series[::self.skip][(x + 1)])
            if y0 == y1:
                self._draw_h_line(y0, x, (x + 1), line=(self.char_set['curve_hl']))
            else:
                self._draw_diag(y0, y1, x)
                start = min(y0, y1) + 1
                end = max(y0, y1)
                self._draw_v_line(start, end, x, line=(self.char_set['curve_vl']))

    def _draw_diag(self, y0, y1, x):
        """Plot diagonal element"""
        if y0 > y1:
            c1 = self.char_set['curve_ar']
            c0 = self.char_set['curve_lb']
        else:
            c1 = self.char_set['curve_br']
            c0 = self.char_set['curve_la']
        self._set_elem(y1, x, c1)
        self._set_elem(y0, x, c0)

    def _draw_h_line(self, y, x_start, x_end, line='-'):
        """Plot horizontal line"""
        for x in range(x_start, x_end):
            self._set_elem(y, x, line)

    def _draw_v_line(self, y_start, y_end, x, line='|'):
        """Plot vertical line"""
        for y in range(y_start, y_end):
            self._set_elem(y, x, line)

    def _set_elem(self, y, x, c):
        """Plot signle element into canvas"""
        self.canvas[(self.rows - y)][x + self.offset] = c

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.canvas])

    __str__ = __repr__