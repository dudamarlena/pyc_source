# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\highcharts\highstock\highstock.py
# Compiled at: 2019-10-14 04:38:55
# Size of source mod 2**32: 18250 bytes
from __future__ import unicode_literals, absolute_import
from future.standard_library import install_aliases
install_aliases()
from jinja2 import Environment, PackageLoader
import json, uuid, re, datetime, html
from collections import Iterable
from .options import BaseOptions, ChartOptions, ColorsOptions, CreditsOptions, ExportingOptions, GlobalOptions, LabelsOptions, LangOptions, LegendOptions, LoadingOptions, NavigatorOptions, NavigationOptions, PlotOptions, RangeSelectorOptions, ScrollbarOptions, SeriesData, SubtitleOptions, TitleOptions, TooltipOptions, xAxisOptions, yAxisOptions, MultiAxis
from .highstock_types import Series, SeriesOptions
from .common import Levels, Formatter, CSSObject, SVGObject, JSfunction, RawJavaScriptText, CommonObject, ArrayObject, ColorObject
CONTENT_FILENAME = './content.html'
PAGE_FILENAME = './page.html'
pl = PackageLoader('highcharts.highstock', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)
template_content = jinja2_env.get_template(CONTENT_FILENAME)
template_page = jinja2_env.get_template(PAGE_FILENAME)

class Highstock(object):
    __doc__ = '\n    Highstock Base class.\n    '
    count = 0
    CHART_FILENAME = None
    template_environment = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

    def __init__(self, **kwargs):
        """
        This is the base class for all the charts. The following keywords are
        accepted:
        :keyword: **display_container** - default: ``True``
        """
        self.model = self.__class__.__name__
        self.div_name = kwargs.get('renderTo', 'container')
        self.template_page_highcharts = template_page
        self.template_content_highcharts = template_content
        self.JSsource = [
         'https://img.highcharts.com.cn/jquery/jquery-1.8.3.min.js',
         'https://img.highcharts.com.cn/highstock/highstock.js',
         'https://img.highcharts.com.cn/highcharts/modules/exporting.js',
         'https://img.highcharts.com.cn/highcharts-plugins/highcharts-zh_CN.js',
         'http://cdn.hcharts.cn/highstock/indicators/indicators.js',
         'http://cdn.hcharts.cn/highstock/indicators/atr.js',
         'http://cdn.hcharts.cn/highstock/indicators/ema.js',
         'http://cdn.hcharts.cn/highstock/indicators/macd.js',
         'https://code.highcharts.com.cn/highstock/indicators/bollinger-bands.js',
         'https://code.highcharts.com.cn/highstock/modules/drag-panes.js']
        self.CSSsource = []
        self.data = []
        self.data_temp = []
        self.navi_seri_flag = False
        self.navi_seri = {}
        self.navi_seri_temp = {}
        self.jsonp_data_flag = False
        self.jsonp_data_url_list = []
        self.jscript_head_flag = False
        self.jscript_head = kwargs.get('jscript_head', None)
        self.jscript_end_flag = False
        self.jscript_end = kwargs.get('jscript_end', None)
        self.div_style = kwargs.get('divstyle', '')
        self.date_flag = kwargs.get('date_flag', False)
        self._htmlcontent = ''
        self.htmlheader = ''
        self.container = ''
        self.containerheader = ''
        self.loading = 'Loading....'
        self.options = {'chart':ChartOptions(), 
         'colors':ColorsOptions(), 
         'credits':CreditsOptions(), 
         'exporting':ExportingOptions(), 
         'labels':LabelsOptions(), 
         'legend':LegendOptions(), 
         'loading':LoadingOptions(), 
         'navigation':NavigationOptions(), 
         'navigator':NavigatorOptions(), 
         'plotOptions':PlotOptions(), 
         'rangeSelector':RangeSelectorOptions(), 
         'scrollbar':ScrollbarOptions(), 
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

    def add_data_set(self, data, series_type='line', name=None, **kwargs):
        """set data for series option in highstocks"""
        self.data_set_count += 1
        if not name:
            name = 'Series %d' % self.data_set_count
        kwargs.update({'name': name})
        kwargs.update({'id': name})
        series_data = Series(data, series_type=series_type, **kwargs)
        series_data.__options__().update(SeriesOptions(series_type=series_type, **kwargs).__options__())
        self.data_temp.append(series_data)

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
        (self.add_data_set)(RawJavaScriptText(self.jsonp_data), series_type, name=name, **kwargs)
        self.jsonp_data_url_list.append(json.dumps(data_src))

    def add_navi_series(self, data, series_type='line', **kwargs):
        """set series for navigator option in highstocks"""
        self.navi_seri_flag = True
        series_data = Series(data, series_type=series_type, **kwargs)
        series_data.__options__().update(SeriesOptions(series_type=series_type, **kwargs).__options__())
        self.navi_seri_temp = series_data

    def add_navi_series_from_jsonp(self, data_src=None, data_name='json_data', series_type='line', **kwargs):
        """set series for navigator option in highstocks"""
        if not self.jsonp_data_flag:
            self.jsonp_data_flag = True
            self.jsonp_data_url = json.dumps(data_src)
            if data_name == 'data':
                data_name = 'json_' + data_name
            self.jsonp_data = data_name
        (self.add_navi_series)((RawJavaScriptText(self.jsonp_data)), series_type, **kwargs)

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
        else:
            if js_loc == 'end':
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
        elif (option_type == 'yAxis' or option_type == 'xAxis') and isinstance(option_dict, list):
            self.options[option_type] = MultiAxis(option_type)
            for each_dict in option_dict:
                (self.options[option_type].update)(**each_dict)

        else:
            if option_type == 'colors':
                self.options['colors'].set_colors(option_dict)
            else:
                if option_type in ('global', 'lang'):
                    (self.setOptions[option_type].update_dict)(**option_dict)
                else:
                    (self.options[option_type].update_dict)(**option_dict)

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
        if self.navi_seri_flag:
            self.navi_seri = json.dumps((self.navi_seri_temp), cls=HighchartsEncoder)
        self._htmlcontent = self.template_content_highcharts.render(chart=self).encode('utf-8')
        i = 1

    def buildhtml(self):
        """build the HTML page
        create the htmlheader with css / js
        create html page
        """
        self.buildcontent()
        self.buildhtmlheader()
        self.content = self._htmlcontent.decode('utf-8')
        finalpagehmtl = self.template_page_highcharts.render(chart=self)
        return finalpagehmtl

    def buildhtmlheader(self):
        """generate HTML header content"""
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
            else:
                return '<iframe style="border:0;outline:none;overflow:hidden" srcdoc="' + htmlsrcdoc + '" height=' + str(height) + ' width=' + str(width) + '></iframe>'
        else:
            return '<iframe style="border:0;outline:none;overflow:hidden" srcdoc="' + htmlsrcdoc + '" height=' + str(height) + ' width=' + str(width) + '></iframe>'

    def __str__(self):
        """return htmlcontent"""
        return self.htmlcontent

    def save_file(self, filename='StockChart'):
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
        else:
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
            else:
                if isinstance(obj, BaseOptions) or isinstance(obj, MultiAxis):
                    return obj.__jsonable__()
                else:
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
            result = result.replace('"%s"' % (k,), v)

        return result


class OptionTypeError(Exception):

    def __init__(self, *args):
        self.args = args