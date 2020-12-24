# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/NVD3Chart.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 19695 bytes
__doc__ = '\nPython-nvd3 is a Python wrapper for NVD3 graph library.\nNVD3 is an attempt to build re-usable charts and chart components\nfor d3.js without taking away the power that d3.js gives you.\n\nProject location : https://github.com/areski/python-nvd3\n'
from __future__ import unicode_literals
from optparse import OptionParser
from jinja2 import Environment, PackageLoader
from airflow._vendor.slugify import slugify
try:
    import simplejson as json
except ImportError:
    import json

CONTENT_FILENAME = './content.html'
PAGE_FILENAME = './page.html'
pl = PackageLoader('airflow._vendor.nvd3', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)
template_content = jinja2_env.get_template(CONTENT_FILENAME)
template_page = jinja2_env.get_template(PAGE_FILENAME)

def stab(tab=1):
    """
    create space tabulation
    """
    return '    ' * tab


class NVD3Chart(object):
    """NVD3Chart"""
    count = 0
    assets_directory = './bower_components/'
    CHART_FILENAME = None
    template_environment = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

    def __init__(self, **kwargs):
        """
        This is the base class for all the charts. The following keywords are
        accepted:

        :keyword: **display_container** - default: ``True``
        :keyword: **jquery_on_ready** - default: ``False``
        :keyword: **charttooltip_dateformat** - default: ``'%d %b %Y'``
        :keyword: **name** - default: the class name
                    ``model`` - set the model (e.g. ``pieChart``, `
                    ``LineWithFocusChart``, ``MultiBarChart``).
        :keyword: **color_category** - default - ``None``
        :keyword: **color_list** - default - ``None``
                  used by pieChart (e.g. ``['red', 'blue', 'orange']``)
        :keyword: **margin_bottom** - default - ``20``
        :keyword: **margin_left** - default - ``60``
        :keyword: **margin_right** - default - ``60``
        :keyword: **margin_top** - default - ``30``
        :keyword: **height** - default - ``''``
        :keyword: **width** - default - ``''``
        :keyword: **stacked** - default - ``False``
        :keyword: **focus_enable** - default - ``False``
        :keyword: **resize** - define - ``False``
        :keyword: **show_legend** - default - ``True``
        :keyword: **show_labels** - default - ``True``
        :keyword: **tag_script_js** - default - ``True``
        :keyword: **use_interactive_guideline** - default - ``False``
        :keyword: **chart_attr** - default - ``None``
        :keyword: **extras** - default - ``None``

            Extra chart modifiers. Use this to modify different attributes of
            the chart.
        :keyword: **x_axis_date** - default - False
            Signal that x axis is a date axis
        :keyword: **date_format** - default - ``%x``
                  see https://github.com/mbostock/d3/wiki/Time-Formatting
        :keyword: **x_axis_format** - default - ``''``.
        :keyword: **y_axis_format** - default - ``''``.
        :keyword: **style** - default - ``''``
            Style modifiers for the DIV container.
        :keyword: **color_category** - default - ``category10``

            Acceptable values are nvd3 categories such as
            ``category10``, ``category20``, ``category20c``.
        """
        self.model = self.__class__.__name__
        self.template_page_nvd3 = template_page
        self.template_content_nvd3 = template_content
        self.series = []
        self.axislist = {}
        self.display_container = kwargs.get('display_container', True)
        self.charttooltip_dateformat = kwargs.get('charttooltip_dateformat', '%d %b %Y')
        self._slugify_name(kwargs.get('name', self.model))
        self.jquery_on_ready = kwargs.get('jquery_on_ready', False)
        self.color_category = kwargs.get('color_category', None)
        self.color_list = kwargs.get('color_list', None)
        self.margin_bottom = kwargs.get('margin_bottom', 20)
        self.margin_left = kwargs.get('margin_left', 60)
        self.margin_right = kwargs.get('margin_right', 60)
        self.margin_top = kwargs.get('margin_top', 30)
        self.height = kwargs.get('height', '')
        self.width = kwargs.get('width', '')
        self.stacked = kwargs.get('stacked', False)
        self.focus_enable = kwargs.get('focus_enable', False)
        self.resize = kwargs.get('resize', False)
        self.show_legend = kwargs.get('show_legend', True)
        self.show_labels = kwargs.get('show_labels', True)
        self.tag_script_js = kwargs.get('tag_script_js', True)
        self.use_interactive_guideline = kwargs.get('use_interactive_guideline', False)
        self.chart_attr = kwargs.get('chart_attr', {})
        self.extras = kwargs.get('extras', None)
        self.style = kwargs.get('style', '')
        self.date_format = kwargs.get('date_format', '%x')
        self.x_axis_date = kwargs.get('x_axis_date', False)
        self.date_flag = kwargs.get('date_flag', False)
        self.x_axis_format = kwargs.get('x_axis_format', '')
        self.remote_js_assets = kwargs.get('remote_js_assets', True)
        self.htmlcontent = ''
        self.htmlheader = ''
        self.container = ''
        self.containerheader = ''
        self.header_css = ['<link href="%s" rel="stylesheet" />' % h for h in (
         'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.0/nv.d3.min.css' if self.remote_js_assets else self.assets_directory + 'nvd3/src/nv.d3.css',)]
        self.header_js = ['<script src="%s"></script>' % h for h in (
         'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js' if self.remote_js_assets else self.assets_directory + 'd3/d3.min.js',
         'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.0/nv.d3.min.js' if self.remote_js_assets else self.assets_directory + 'nvd3/nv.d3.min.js')]
        self.jschart = None
        self.custom_tooltip_flag = False
        self.tooltip_condition_string = ''
        self.charttooltip = ''
        self.serie_no = 1

    def _slugify_name(self, name):
        """Slufigy name with underscore"""
        self.name = slugify(name, separator='_')

    def add_serie(self, y, x, name=None, extra=None, **kwargs):
        """
        add serie - Series are list of data that will be plotted
        y {1, 2, 3, 4, 5} / x {1, 2, 3, 4, 5}

        **Attributes**:

            * ``name`` - set Serie name
            * ``x`` - x-axis data
            * ``y`` - y-axis data

            kwargs:

            * ``shape`` - for scatterChart, you can set different shapes
                          (circle, triangle etc...)
            * ``size`` - for scatterChart, you can set size of different shapes
            * ``type`` - for multiChart, type should be bar
            * ``bar`` - to display bars in Chart
            * ``color_list`` - define list of colors which will be
                               used by pieChart
            * ``color`` - set axis color
            * ``disabled`` -

            extra:

            * ``tooltip`` - set tooltip flag
            * ``date_format`` - set date_format for tooltip if x-axis is in
              date format

        """
        if not name:
            name = 'Serie %d' % self.serie_no
        else:
            if 'shape' in kwargs or 'size' in kwargs:
                csize = kwargs.get('size', 1)
                cshape = kwargs.get('shape', 'circle')
                serie = [{'x':x[i],  'y':j,  'shape':cshape,  'size':csize[i] if isinstance(csize, list) else csize} for i, j in enumerate(y)]
            else:
                if self.model == 'pieChart':
                    serie = [{'label':x[i],  'value':y} for i, y in enumerate(y)]
                else:
                    serie = [{'x':x[i],  'y':y} for i, y in enumerate(y)]
                data_keyvalue = {'values':serie, 
                 'key':name}
                if 'type' in kwargs:
                    if kwargs['type']:
                        data_keyvalue['type'] = kwargs['type']
                if 'yaxis' in kwargs:
                    if kwargs['yaxis']:
                        data_keyvalue['yAxis'] = kwargs['yaxis']
                if self.model != 'pieChart':
                    data_keyvalue['yAxis'] = '1'
                if 'bar' in kwargs:
                    if kwargs['bar']:
                        data_keyvalue['bar'] = 'true'
                if 'disabled' in kwargs:
                    if kwargs['disabled']:
                        data_keyvalue['disabled'] = 'true'
                if 'color' in kwargs:
                    if kwargs['color']:
                        data_keyvalue['color'] = kwargs['color']
                if extra:
                    if self.model == 'pieChart':
                        if 'color_list' in extra:
                            if extra['color_list']:
                                self.color_list = extra['color_list']
                    if extra.get('date_format'):
                        self.charttooltip_dateformat = extra['date_format']
                    if extra.get('tooltip'):
                        self.custom_tooltip_flag = True
                        if self.model != 'pieChart':
                            _start = extra['tooltip']['y_start']
                            _end = extra['tooltip']['y_end']
                            _start = "'" + str(_start) + "' + " if _start else ''
                            _end = " + '" + str(_end) + "'" if _end else ''
                            if self.model == 'linePlusBarChart':
                                if self.tooltip_condition_string:
                                    self.tooltip_condition_string += stab(5)
                                self.tooltip_condition_string += stab(0) + "if(key.indexOf('" + name + "') > -1 ){\n" + stab(6) + 'var y = ' + _start + ' String(graph.point.y) ' + _end + ';\n' + stab(5) + '}\n'
                            else:
                                if self.model == 'cumulativeLineChart':
                                    self.tooltip_condition_string += stab(0) + "if(key == '" + name + "'){\n" + stab(6) + 'var y = ' + _start + ' String(e) ' + _end + ';\n' + stab(5) + '}\n'
                                else:
                                    self.tooltip_condition_string += stab(5) + "if(key == '" + name + "'){\n" + stab(6) + 'var y = ' + _start + ' String(graph.point.y) ' + _end + ';\n' + stab(5) + '}\n'
                        if self.model == 'pieChart':
                            _start = extra['tooltip']['y_start']
                            _end = extra['tooltip']['y_end']
                            _start = "'" + str(_start) + "' + " if _start else ''
                            _end = " + '" + str(_end) + "'" if _end else ''
                            self.tooltip_condition_string += 'var y = ' + _start + ' String(y) ' + _end + ';\n'
        self.serie_no += 1
        self.series.append(data_keyvalue)

    def add_chart_extras(self, extras):
        """
        Use this method to add extra d3 properties to your chart.
        For example, you want to change the text color of the graph::

            chart = pieChart(name='pieChart', color_category='category20c', height=400, width=400)

            xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
            ydata = [3, 4, 0, 1, 5, 7, 3]

            extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
            chart.add_serie(y=ydata, x=xdata, extra=extra_serie)

        The above code will create graph with a black text, the following will change it::

            text_white="d3.selectAll('#pieChart text').style('fill', 'white');"
            chart.add_chart_extras(text_white)

        The above extras will be appended to the java script generated.

        Alternatively, you can use the following initialization::

            chart = pieChart(name='pieChart',
                             color_category='category20c',
                             height=400, width=400,
                             extras=text_white)
        """
        self.extras = extras

    def set_graph_height(self, height):
        """Set Graph height"""
        self.height = str(height)

    def set_graph_width(self, width):
        """Set Graph width"""
        self.width = str(width)

    def set_containerheader(self, containerheader):
        """Set containerheader"""
        self.containerheader = containerheader

    def set_date_flag(self, date_flag=False):
        """Set date flag"""
        self.date_flag = date_flag

    def set_custom_tooltip_flag(self, custom_tooltip_flag):
        """Set custom_tooltip_flag & date_flag"""
        self.custom_tooltip_flag = custom_tooltip_flag

    def __str__(self):
        """return htmlcontent"""
        self.buildhtml()
        return self.htmlcontent

    def buildcontent(self):
        """Build HTML content only, no header or body tags. To be useful this
        will usually require the attribute `juqery_on_ready` to be set which
        will wrap the js in $(function(){<regular_js>};)
        """
        self.buildcontainer()
        self.buildjschart()
        self.htmlcontent = self.template_content_nvd3.render(chart=self)

    def buildhtml(self):
        """Build the HTML page
        Create the htmlheader with css / js
        Create html page
        Add Js code for nvd3
        """
        self.buildcontent()
        self.content = self.htmlcontent
        self.htmlcontent = self.template_page_nvd3.render(chart=self)

    def buildhtmlheader(self):
        """generate HTML header content"""
        self.htmlheader = ''
        if '_js_initialized' not in globals() or not _js_initialized:
            for css in self.header_css:
                self.htmlheader += css

            for js in self.header_js:
                self.htmlheader += js

    def buildcontainer(self):
        """generate HTML div"""
        if self.container:
            return
        else:
            if self.width:
                if self.width[(-1)] != '%':
                    self.style += 'width:%spx;' % self.width
                else:
                    self.style += 'width:%s;' % self.width
            if self.height:
                if self.height[(-1)] != '%':
                    self.style += 'height:%spx;' % self.height
                else:
                    self.style += 'height:%s;' % self.height
            if self.style:
                self.style = 'style="%s"' % self.style
        self.container = self.containerheader + '<div id="%s"><svg %s></svg></div>\n' % (self.name, self.style)

    def buildjschart(self):
        """generate javascript code for the chart"""
        self.jschart = ''
        if self.tooltip_condition_string == '':
            self.tooltip_condition_string = 'var y = String(graph.point.y);\n'
        self.series_js = json.dumps(self.series)

    def create_x_axis(self, name, label=None, format=None, date=False, custom_format=False):
        """Create X-axis"""
        axis = {}
        if custom_format:
            if format:
                axis['tickFormat'] = format
        if format:
            if format == 'AM_PM':
                axis['tickFormat'] = 'function(d) { return get_am_pm(parseInt(d)); }'
            else:
                axis['tickFormat'] = "d3.format(',%s')" % format
        if label:
            axis['axisLabel'] = "'" + label + "'"
        if date:
            self.dateformat = format
            axis['tickFormat'] = "function(d) { return d3.time.format('%s')(new Date(parseInt(d))) }\n" % self.dateformat
            if name[0] == 'x':
                self.x_axis_date = True
        self.axislist[name] = axis
        if name == 'xAxis':
            if self.focus_enable:
                self.axislist['x2Axis'] = axis

    def create_y_axis(self, name, label=None, format=None, custom_format=False):
        """
        Create Y-axis
        """
        axis = {}
        if custom_format:
            if format:
                axis['tickFormat'] = format
        if format:
            axis['tickFormat'] = "d3.format(',%s')" % format
        if label:
            axis['axisLabel'] = "'" + label + "'"
        self.axislist[name] = axis


class TemplateMixin(object):
    """TemplateMixin"""

    def buildcontent(self):
        """Build HTML content only, no header or body tags. To be useful this
        will usually require the attribute `juqery_on_ready` to be set which
        will wrap the js in $(function(){<regular_js>};)
        """
        self.buildcontainer()
        self.buildjschart()
        self.htmlcontent = self.template_chart_nvd3.render(chart=self)


def _main():
    """
    Parse options and process commands
    """
    usage = 'usage: nvd3.py [options]'
    parser = OptionParser(usage=usage, version='python-nvd3 - Charts generator with nvd3.js and d3.js')
    parser.add_option('-q', '--quiet', action='store_false',
      dest='verbose',
      default=True,
      help="don't print messages to stdout")
    options, args = parser.parse_args()


if __name__ == '__main__':
    _main()