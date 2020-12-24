# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\highcharts\highcharts\highcharts.py
# Compiled at: 2019-06-05 03:25:47
# Size of source mod 2**32: 17749 bytes
from __future__ import unicode_literals, absolute_import
from future.standard_library import install_aliases
install_aliases()
from past.builtins import basestring
from jinja2 import Environment, PackageLoader
import json, uuid, re, datetime, urllib.request, urllib.error, urllib.parse, html
from collections import Iterable
from .options import BaseOptions, ChartOptions, ColorAxisOptions, ColorsOptions, CreditsOptions, DrilldownOptions, ExportingOptions, GlobalOptions, LabelsOptions, LangOptions, LegendOptions, LoadingOptions, NavigationOptions, PaneOptions, PlotOptions, SeriesData, SubtitleOptions, TitleOptions, TooltipOptions, xAxisOptions, yAxisOptions, zAxisOptions, MultiAxis
from .highchart_types import Series, SeriesOptions
from .common import Levels, Formatter, CSSObject, SVGObject, JSfunction, RawJavaScriptText, CommonObject, ArrayObject, ColorObject
CONTENT_FILENAME = 'content.html'
PAGE_FILENAME = 'page.html'
pl = PackageLoader('highcharts.highcharts', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)
template_content = jinja2_env.get_template(CONTENT_FILENAME)
template_page = jinja2_env.get_template(PAGE_FILENAME)

class Highchart(object):
    __doc__ = '\n    Highcharts Base class.\n    '
    count = 0
    CHART_FILENAME = None
    template_environment = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

    def __init__(self, **kwargs):
        """
        This is the base class for all the charts. The following keywords are
        accepted:
        :keyword: **display_container** - default: ``True``
                  **offline - default: ``False``
                            If True, download all .js and .css file and put them
                            into the generated .html so it can be viewed offline.
        """
        self.model = self.__class__.__name__
        self.div_name = kwargs.get('renderTo', 'container')
        self.template_page_highcharts = template_page
        self.template_content_highcharts = template_content
        self.JSsource = [
         'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
         'https://code.highcharts.com/6/highcharts.js',
         'https://code.highcharts.com/6/highcharts-more.js',
         'https://code.highcharts.com/6/modules/heatmap.js',
         'https://code.highcharts.com/6/modules/exporting.js']
        self.CSSsource = [
         'https://www.highcharts.com/highslide/highslide.css']
        self.offline = kwargs.get('offline', False)
        self.data = []
        self.data_temp = []
        self.jsonp_data_flag = False
        self.jsonp_data_url_list = []
        self.drilldown_data = []
        self.drilldown_data_temp = []
        self.jscript_head_flag = False
        self.jscript_head = kwargs.get('jscript_head', None)
        self.jscript_end_flag = False
        self.jscript_end = kwargs.get('jscript_end', None)
        self.div_style = kwargs.get('style', '')
        self.drilldown_flag = kwargs.get('drilldown_flag', False)
        self._htmlcontent = ''
        self.htmlheader = ''
        self.container = ''
        self.containerheader = ''
        self.loading = 'Loading....'
        self.options = {'chart':ChartOptions(), 
         'colors':ColorsOptions(), 
         'credits':CreditsOptions(), 
         'drilldown':DrilldownOptions(), 
         'exporting':ExportingOptions(), 
         'labels':LabelsOptions(), 
         'legend':LegendOptions(), 
         'loading':LoadingOptions(), 
         'navigation':NavigationOptions(), 
         'pane':PaneOptions(), 
         'plotOptions':PlotOptions(), 
         'series':SeriesData(), 
         'subtitle':SubtitleOptions(), 
         'title':TitleOptions(), 
         'tooltip':TooltipOptions(), 
         'xAxis':xAxisOptions(), 
         'yAxis':yAxisOptions()}
        self.setOptions = {'global':GlobalOptions(), 
         'lang':LangOptions()}
        self.__load_defaults__()
        allowed_kwargs = [
         'width',
         'height',
         'renderTo',
         'backgroundColor',
         'events',
         'marginBottom',
         'marginTop',
         'marginRight',
         'marginLeft']
        for keyword in allowed_kwargs:
            if keyword in kwargs:
                (self.options['chart'].update_dict)(**{keyword: kwargs[keyword]})

        self.data_set_count = 0
        self.drilldown_data_set_count = 0

    def __load_defaults__(self):
        self.options['chart'].update_dict(renderTo='container')
        self.options['title'].update_dict(text='A New Highchart')
        self.options['credits'].update_dict(enabled=False)

    def add_JSsource(self, new_src):
        """add additional js script source(s)"""
        if isinstance(new_src, list):
            for h in new_src:
                self.JSsource.append(h)

        else:
            if isinstance(new_src, basestring):
                self.JSsource.append(new_src)
            else:
                raise OptionTypeError('Option: %s Not Allowed For Series Type: %s' % type(new_src))

    def add_CSSsource(self, new_src):
        """add additional css source(s)"""
        if isinstance(new_src, list):
            for h in new_src:
                self.CSSsource.append(h)

        else:
            if isinstance(new_src, basestring):
                self.CSSsource.append(new_src)
            else:
                raise OptionTypeError('Option: %s Not Allowed For Series Type: %s' % type(new_src))

    def add_3d_rotation(self):
        self.options3d_rotation_flag = True

    def add_data_set(self, data, series_type='line', name=None, **kwargs):
        """set data for series option in highcharts"""
        self.data_set_count += 1
        if not name:
            name = 'Series %d' % self.data_set_count
        kwargs.update({'name': name})
        if series_type == 'treemap':
            self.add_JSsource('http://code.highcharts.com/modules/treemap.js')
        series_data = Series(data, series_type=series_type, **kwargs)
        series_data.__options__().update(SeriesOptions(series_type=series_type, **kwargs).__options__())
        self.data_temp.append(series_data)

    def add_drilldown_data_set(self, data, series_type, id, **kwargs):
        """set data for drilldown option in highcharts"""
        self.drilldown_data_set_count += 1
        if self.drilldown_flag == False:
            self.drilldown_flag = True
        kwargs.update({'id': id})
        series_data = Series(data, series_type=series_type, **kwargs)
        series_data.__options__().update(SeriesOptions(series_type=series_type, **kwargs).__options__())
        self.drilldown_data_temp.append(series_data)

    def add_data_from_jsonp(self, data_src, data_name='json_data', series_type='line', name=None, **kwargs):
        """set map data directly from a https source
        the data_src is the https link for data
        and it must be in jsonp format
        """
        if not self.jsonp_data_flag:
            self.jsonp_data_flag = True
            if data_name == 'data':
                data_name = 'json_' + data_name
            self.jsonp_data = data_name
        (self.add_data_set)(RawJavaScriptText(data_name), series_type, name=name, **kwargs)
        self.jsonp_data_url_list.append(json.dumps(data_src))

    def add_JSscript(self, js_script, js_loc):
        """add (highcharts) javascript in the beginning or at the end of script
        use only if necessary
        """
        if js_loc == 'head':
            self.jscript_head_flag = True
            if self.jscript_head:
                self.jscript_head = self.jscript_head + '\n' + js_script
            else:
                self.jscript_head = js_script
        elif js_loc == 'end':
            self.jscript_end_flag = True
            if self.jscript_end:
                self.jscript_end = self.jscript_end + '\n' + js_script
            else:
                self.jscript_end = js_script
        else:
            raise OptionTypeError("Not An Accepted script location: %s, either 'head' or 'end'" % js_loc)

    def set_options(self, option_type, option_dict, force_options=False):
        """set plot options """
        if force_options:
            self.options[option_type].update(option_dict)
        else:
            if option_type == 'yAxis' or option_type == 'xAxis':
                if isinstance(option_dict, list):
                    self.options[option_type] = MultiAxis(option_type)
                    for each_dict in option_dict:
                        (self.options[option_type].update)(**each_dict)

                else:
                    if option_type == 'colors':
                        self.options['colors'].set_colors(option_dict)
                    else:
                        if option_type == 'zAxis':
                            self.options.update({'zAxis': zAxisOptions()})
                            (self.options[option_type].update_dict)(**option_dict)
                        else:
                            if option_type in ('global', 'lang'):
                                (self.setOptions[option_type].update_dict)(**option_dict)
                            else:
                                if option_type == 'colorAxis':
                                    self.options.update({'colorAxis': ColorAxisOptions()})
                                    (self.options[option_type].update_dict)(**option_dict)
                                else:
                                    (self.options[option_type].update_dict)(**option_dict)
            elif option_type == 'chart' and 'options3d' in option_dict:
                self.add_JSsource('http://code.highcharts.com/highcharts-3d.js')

    def set_dict_options(self, options):
        """for dictionary-like inputs (as object in Javascript)
        options must be in python dictionary format
        """
        if isinstance(options, dict):
            for key, option_data in options.items():
                self.set_options(key, option_data)

        else:
            raise OptionTypeError('Not An Accepted Input Format: %s. Must be Dictionary' % type(options))

    def buildcontent(self):
        """build HTML content only, no header or body tags"""
        self.buildcontainer()
        self.option = json.dumps((self.options), cls=HighchartsEncoder)
        self.setoption = json.dumps((self.setOptions), cls=HighchartsEncoder)
        self.data = json.dumps((self.data_temp), cls=HighchartsEncoder)
        self.data_list = [json.dumps(x, cls=HighchartsEncoder) for x in self.data_temp]
        if self.drilldown_flag:
            self.drilldown_data = json.dumps((self.drilldown_data_temp), cls=HighchartsEncoder)
        self._htmlcontent = self.template_content_highcharts.render(chart=self).encode('utf-8')

    def buildhtml(self):
        """build the HTML page
        create the htmlheader with css / js
        create html page
        """
        self.buildcontent()
        self.buildhtmlheader()
        self.content = self._htmlcontent.decode('utf-8')
        self._htmlcontent = self.template_page_highcharts.render(chart=self)
        return self._htmlcontent

    def buildhtmlheader(self):
        """generate HTML header content"""
        if self.drilldown_flag:
            self.add_JSsource('http://code.highcharts.com/modules/drilldown.js')
        elif self.offline:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            self.header_css = ['<style>%s</style>' % opener.open(h).read() for h in self.CSSsource]
            self.header_js = ['<script type="text/javascript">%s</script>' % opener.open(h).read() for h in self.JSsource]
        else:
            self.header_css = ['<link href="%s" rel="stylesheet" />' % h for h in self.CSSsource]
            self.header_js = ['<script type="text/javascript" src="%s"></script>' % h for h in self.JSsource]
        self.htmlheader = ''
        for css in self.header_css:
            self.htmlheader += css

        for js in self.header_js:
            self.htmlheader += js

    def buildcontainer(self):
        """generate HTML div"""
        if self.container:
            return
            if self.options['chart'].width:
                if str(self.options['chart'].width)[(-1)] != '%':
                    self.div_style += 'width:%spx;' % self.options['chart'].width
                else:
                    self.div_style += 'width:%s;' % self.options['chart'].width
            if self.options['chart'].height:
                if str(self.options['chart'].height)[(-1)] != '%':
                    self.div_style += 'height:%spx;' % self.options['chart'].height
        else:
            self.div_style += 'height:%s;' % self.options['chart'].height
        self.div_name = self.options['chart'].__dict__['renderTo']
        self.container = self.containerheader + '<div id="%s" style="%s">%s</div>\n' % (self.div_name, self.div_style, self.loading)

    @property
    def htmlcontent(self):
        return self.buildhtml()

    @property
    def iframe(self):
        htmlsrcdoc = html.escape(self.htmlcontent)
        htmlsrcdoc = re.sub('\\n', ' ', htmlsrcdoc)
        htmlsrcdoc = re.sub(' +', ' ', htmlsrcdoc)
        width = int(self.options['chart'].__dict__['width']) if self.options['chart'].__dict__.get('width') else 820
        height = int(self.options['chart'].__dict__['height']) if self.options['chart'].__dict__.get('height') else 520
        if self.options['chart'].__dict__.get('options3d'):
            if len(htmlsrcdoc) < 99965000:
                return '<iframe style="border:0;outline:none;overflow:hidden" src="data:text/html,' + htmlsrcdoc + '" height=' + str(height) + ' width=' + str(width) + '></iframe>'
            return '<iframe style="border:0;outline:none;overflow:hidden" srcdoc="' + htmlsrcdoc + '" height=' + str(height) + ' width=' + str(width) + '></iframe>'
        else:
            return '<iframe style="border:0;outline:none;overflow:hidden" srcdoc="' + htmlsrcdoc + '" height=' + str(height) + ' width=' + str(width) + '></iframe>'

    def __str__(self):
        """return htmlcontent"""
        return self.htmlcontent

    def save_file(self, filename='Chart'):
        """ save htmlcontent as .html file """
        filename = filename + '.html'
        with open(filename, 'w') as (f):
            f.write(self.htmlcontent)
        f.closed


class HighchartsEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        (json.JSONEncoder.__init__)(self, *args, **kwargs)
        self._replacement_map = {}

    def default(self, obj):
        if isinstance(obj, RawJavaScriptText):
            key = uuid.uuid4().hex
            self._replacement_map[key] = obj.get_jstext()
            return key
        if isinstance(obj, datetime.datetime):
            utc = obj.utctimetuple()
            obj = 'Date.UTC({year},{month},{day},{hours},{minutes},{seconds},{millisec})'.format(year=(utc[0]),
              month=(utc[1] - 1),
              day=(utc[2]),
              hours=(utc[3]),
              minutes=(utc[4]),
              seconds=(utc[5]),
              millisec=(obj.microsecond / 1000))
            return RawJavaScriptText(obj)
        if isinstance(obj, BaseOptions) or isinstance(obj, MultiAxis):
            return obj.__jsonable__()
        if isinstance(obj, CSSObject) or isinstance(obj, Formatter) or isinstance(obj, JSfunction):
            return obj.__jsonable__()
        if isinstance(obj, SeriesOptions) or isinstance(obj, Series):
            return obj.__jsonable__()
        if isinstance(obj, CommonObject) or isinstance(obj, ArrayObject) or isinstance(obj, ColorObject):
            return obj.__jsonable__()
        return json.JSONEncoder.default(self, obj)

    def encode(self, obj):
        result = json.JSONEncoder.encode(self, obj)
        for k, v in self._replacement_map.items():
            result = result.replace('"{}"'.format(k), v)

        return result


class OptionTypeError(Exception):

    def __init__(self, *args):
        self.args = args