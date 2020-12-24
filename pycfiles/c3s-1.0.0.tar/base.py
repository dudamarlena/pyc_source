# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ben/Documents/Projects/C3PyO/c3pyo/base.py
# Compiled at: 2016-12-08 12:42:40
from __future__ import unicode_literals
import webbrowser, os, json, numbers, re, tempfile, shutil
from jinja2 import Environment, PackageLoader
from c3pyo.utils import single_letter_color_mapping, color_mapping
__here__ = os.path.dirname(os.path.abspath(__file__))
CHART_BASE_FILENAME = b'./chart.html'
pl = PackageLoader(b'c3pyo', b'templates')
jinja2_env = Environment(loader=pl)

class C3Chart(object):
    """
    C3Chart Base Class
    """

    def __init__(self, **kwargs):
        self._chart_type = None
        self._data = None
        self._name = kwargs.get(b'name', b'C3 Chart')
        self._show_points = kwargs.get(b'show_points', True)
        self._show_legend = kwargs.get(b'show_legend', True)
        self._show_legend_position = kwargs.get(b'legend_position', b'bottom')
        self._label_for_x = kwargs.get(b'xlabel', None)
        self._label_for_y = kwargs.get(b'ylabel', None)
        self._x_grid_lines = kwargs.get(b'gridlines', False)
        self._y_grid_lines = kwargs.get(b'gridlines', False)
        self._show_area = kwargs.get(b'area', False)
        self._zoom_on_off = kwargs.get(b'zoom', False)
        self._show_subchart = kwargs.get(b'subchart', False)
        self._height_value = kwargs.get(b'height', 0)
        self._width_value = kwargs.get(b'width', 0)
        self._y_max = kwargs.get(b'y_max', None)
        self._y_min = kwargs.get(b'y_min', None)
        self._show_tooltip = kwargs.get(b'tooltip', True)
        self._chart_div = (b'#{}').format(kwargs.get(b'chart_div', b'chart_div'))
        self._colors = {}
        self._types = {}
        self._save_output = False
        return

    def xlabel(self, label):
        self._label_for_x = label

    def ylabel(self, label):
        self._label_for_y = label

    def area(self, show_area):
        if not isinstance(show_area, bool):
            raise TypeError((b'arg for area must be boolean, received {}').format(type(show_area)))
        self._show_area = show_area

    def legend(self, show_legend):
        if not isinstance(show_legend, bool):
            raise TypeError((b'arg for legend must be boolean, received {}').format(type(show_legend)))
        self._show_legend = show_legend

    def zoom(self, zoom_on_off):
        if not isinstance(zoom_on_off, bool):
            raise TypeError((b'arg for zoom must be boolean, received {}').format(type(zoom_on_off)))
        self._zoom_on_off = zoom_on_off

    def subchart(self, show_subchart):
        if not isinstance(show_subchart, bool):
            raise TypeError((b'arg for subchart must be boolean, received {}').format(type(show_subchart)))
        self._show_subchart = show_subchart

    def height(self, height_value):
        msg = (b'height must be a number, received {} of type {}').format(height_value, type(height_value))
        if isinstance(height_value, bool):
            raise TypeError(msg)
        if not isinstance(height_value, numbers.Number):
            raise TypeError(msg)
        self._height_value = height_value

    def width(self, width_value):
        msg = (b'width must be a number, received {} of type {}').format(width_value, type(width_value))
        if isinstance(width_value, bool):
            raise TypeError(msg)
        if not isinstance(width_value, numbers.Number):
            raise TypeError(msg)
        self._width_value = width_value

    def y_range(self, y_min=None, y_max=None):
        if (not isinstance(y_min, numbers.Number) or isinstance(y_min, bool)) and y_min is not None:
            raise TypeError((b'y_min must be a number, received {} of type {}').format(y_min, type(y_min)))
        if (not isinstance(y_max, numbers.Number) or isinstance(y_max, bool)) and y_max is not None:
            raise TypeError((b'y_max must be a number, received {} of type {}').format(y_max, type(y_max)))
        if y_min is not None:
            self._y_min = y_min
        if y_max is not None:
            self._y_max = y_max
        return

    def gridlines(self, x=None, y=None):
        msg = b'arg for {} gridlines must be boolean, received {}'
        if x is not None:
            if not isinstance(x, bool):
                raise TypeError(msg.format(b'x', type(x)))
            else:
                self._x_grid_lines = x
        if y is not None:
            if not isinstance(y, bool):
                raise TypeError(msg.format(b'y', type(y)))
            self._y_grid_lines = y
        return

    def legend_position(self, position):
        if position not in ('bottom', 'right', 'inset'):
            raise ValueError(b'Currently only bottom, right and inset supported for legend_position')
        self._show_legend_position = position

    def tooltip(self, show_tooltip):
        if not isinstance(show_tooltip, bool):
            raise TypeError((b'arg for show_tooltip must be boolean, received {}').format(type(show_tooltip)))
        self._show_tooltip = show_tooltip

    def bind_to(self, div_name):
        if not isinstance(x, basestring):
            msg = b'parameter for bind_to must be string, received {} of type {}'
            raise TypeError(msg.format(div_name, type(div_name)))
        if div_name.startswith(b'#'):
            self._chart_div = div_name
        else:
            self._chart_div = (b'#{}').format(div_name)

    def add_color(self, color, y_label):
        three_hex = re.compile(b'^(#)?[A-Fa-f0-9]{3}$')
        six_hex = re.compile(b'^(#)?[A-Fa-f0-9]{6}$')
        if color.lower() in single_letter_color_mapping:
            self._colors[y_label] = single_letter_color_mapping[color.lower()]
        elif color.lower() in color_mapping:
            self._colors[y_label] = color_mapping[color.lower()]
        elif three_hex.match(color) or six_hex.match(color):
            if color.startswith(b'#'):
                self._colors[y_label] = color
            else:
                self._colors[y_label] = (b'#{}').format(color)
        else:
            msg = b'color {} not recognised for {}, please use a recognised color or hex code'
            raise ValueError(msg.format(color, y_label))

    def get_legend_for_json(self):
        return {b'show': self._show_legend, 
           b'position': self._show_legend_position}

    def get_grid_for_json(self):
        grid = {b'x': {b'show': self._x_grid_lines}, 
           b'y': {b'show': self._y_grid_lines}}
        if self._chart_type == b'bar':
            grid[b'y'][b'lines'] = [{b'value': 0}]
        return grid

    def get_zoom_for_json(self):
        zoom = {b'enabled': self._zoom_on_off}
        return zoom

    def get_subchart_for_json(self):
        subchart = {b'enabled': self._show_subchart}
        return subchart

    def get_size_for_json(self):
        size = {}
        if self._height_value:
            size[b'height'] = self._height_value
        if self._width_value:
            size[b'width'] = self._width_value
        return size

    def get_points_for_json(self):
        return {b'show': self._show_points}

    def get_tooltip_for_json(self):
        return {b'show': self._show_tooltip}

    def get_donut_for_json(self):
        return {}

    def get_bar_for_json(self):
        return {}

    def plot_graph(self, chart_json):
        directory_name = tempfile.mkdtemp()
        template = jinja2_env.get_template(CHART_BASE_FILENAME)
        temp_path = os.path.join(directory_name, b'chart.html')
        with open(temp_path, b'w') as (f):
            f.write(template.render(title=self._name, chart_json=chart_json))
        shutil.copytree(os.path.join(__here__, b'static'), os.path.join(directory_name, b'static'))
        url = b'file:///' + temp_path
        webbrowser.open(url)

    def json(self):
        res = self.get_chart_json()
        return res

    def get_chart_json(self):
        chart_json = {b'bindto': self._chart_div, 
           b'data': self.get_data_for_json(), 
           b'legend': self.get_legend_for_json(), 
           b'grid': self.get_grid_for_json(), 
           b'axis': self.get_axis_for_json(), 
           b'zoom': self.get_zoom_for_json(), 
           b'subchart': self.get_subchart_for_json(), 
           b'size': self.get_size_for_json(), 
           b'points': self.get_points_for_json(), 
           b'donut': self.get_donut_for_json(), 
           b'tooltip': self.get_tooltip_for_json(), 
           b'bar': self.get_bar_for_json()}
        chart_json = json.dumps(chart_json)
        return chart_json

    def show(self):
        chart_json = self.get_chart_json()
        self.plot_graph(chart_json)

    def get_data_for_json(self):
        raise NotImplementedError

    def get_axis_for_json(self):
        raise NotImplementedError