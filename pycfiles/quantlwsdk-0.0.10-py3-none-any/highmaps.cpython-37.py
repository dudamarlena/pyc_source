# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\highcharts\highmaps\highmaps.py
# Compiled at: 2019-06-05 03:25:48
# Size of source mod 2**32: 19014 bytes
from __future__ import unicode_literals, absolute_import
from future.standard_library import install_aliases
install_aliases()
from past.builtins import basestring
from urllib.request import urlopen
from jinja2 import Environment, PackageLoader
import json, uuid, re, datetime, html
from collections import Iterable
from .options import BaseOptions, ChartOptions, ColorsOptions, ColorAxisOptions, CreditsOptions, DrilldownOptions, ExportingOptions, GlobalOptions, LabelsOptions, LangOptions, LegendOptions, LoadingOptions, MapNavigationOptions, NavigationOptions, PaneOptions, PlotOptions, SeriesData, SubtitleOptions, TitleOptions, TooltipOptions, xAxisOptions, yAxisOptions
from .highmap_types import Series, SeriesOptions
from .common import Formatter, CSSObject, SVGObject, MapObject, JSfunction, RawJavaScriptText, CommonObject, ArrayObject, ColorObject
CONTENT_FILENAME = './content.html'
PAGE_FILENAME = './page.html'
pl = PackageLoader('highcharts.highmaps', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)
template_content = jinja2_env.get_template(CONTENT_FILENAME)
template_page = jinja2_env.get_template(PAGE_FILENAME)

class Highmap(object):
    __doc__ = '\n    Highcharts Base class.\n    '
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
         'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
         'https://code.highcharts.com/maps/6/highmaps.js',
         'https://code.highcharts.com/6/highcharts.js',
         'https://code.highcharts.com/maps/6/modules/map.js',
         'https://code.highcharts.com/maps/6/modules/data.js',
         'https://code.highcharts.com/maps/6/modules/exporting.js']
        self.CSSsource = [
         'https://www.highcharts.com/highslide/highslide.css']
        self.data = []
        self.data_temp = []
        self.data_is_coordinate = False
        self.jsonp_data_flag = False
        self.drilldown_data = []
        self.drilldown_data_temp = []
        self.mapdata_flag = False
        self.map = None
        self.jsonp_map_flag = kwargs.get('jsonp_map_flag', False)
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
         'mapNavigation':MapNavigationOptions(), 
         'navigation':NavigationOptions(), 
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

    def add_data_set(self, data, series_type='map', name=None, is_coordinate=False, **kwargs):
        """set data for series option in highmaps """
        self.data_set_count += 1
        if not name:
            name = 'Series %d' % self.data_set_count
        kwargs.update({'name': name})
        if is_coordinate:
            self.data_is_coordinate = True
            self.add_JSsource('https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.6/proj4.js')
            if self.map:
                if not self.data_temp:
                    series_data = Series([], series_type='map', **{'mapData': self.map})
                    series_data.__options__().update(SeriesOptions(series_type='map', **{'mapData': self.map}).__options__())
                    self.data_temp.append(series_data)
        if self.map:
            if 'mapData' in kwargs.keys():
                kwargs.update({'mapData': self.map})
        series_data = Series(data, series_type=series_type, **kwargs)
        series_data.__options__().update(SeriesOptions(series_type=series_type, **kwargs).__options__())
        self.data_temp.append(series_data)

    def add_drilldown_data_set(self, data, series_type, id, **kwargs):
        """set data for drilldown option in highmaps 
        id must be input and corresponding to drilldown arguments in data series 
        """
        self.drilldown_data_set_count += 1
        if self.drilldown_flag == False:
            self.drilldown_flag = True
        kwargs.update({'id': id})
        series_data = Series(data, series_type=series_type, **kwargs)
        series_data.__options__().update(SeriesOptions(series_type=series_type, **kwargs).__options__())
        self.drilldown_data_temp.append(series_data)

    def add_data_from_jsonp(self, data_src, data_name='json_data', series_type='map', name=None, **kwargs):
        """add data directly from a https source
        the data_src is the https link for data using jsonp
        """
        self.jsonp_data_flag = True
        self.jsonp_data_url = json.dumps(data_src)
        if data_name == 'data':
            data_name = 'json_' + data_name
        self.jsonp_data = data_name
        (self.add_data_set)(RawJavaScriptText(data_name), series_type, name=name, **kwargs)

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

    def add_map_data(self, geojson, **kwargs):
        self.mapdata_flag = True
        self.map = 'geojson'
        self.mapdata = json.dumps(geojson)
        if self.data_is_coordinate:
            kwargs.update({'mapData': self.map})
            series_data = Series([], 'map')
            series_data.__options__().update(SeriesOptions(*('map', ), **kwargs).__options__())
            self.data_temp.append(series_data)
        else:
            if kwargs:
                kwargs.update({'mapData': self.map})
                series_data = Series([], 'map')
                series_data.__options__().update(SeriesOptions(*('map', ), **kwargs).__options__())
                self.data_temp.append(series_data)
            else:
                if self.data_temp:
                    self.data_temp[0].__options__().update({'mapData': MapObject(self.map)})

    def set_map_source(self, map_src, jsonp_map=False):
        """set map data 
        use if the mapData is loaded directly from a https source
        the map_src is the https link for the mapData
        geojson (from jsonp) or .js formates are acceptable
        default is js script from highcharts' map collection: https://code.highcharts.com/mapdata/
        """
        if not map_src:
            raise OptionTypeError('No map source input, please refer to: https://code.highcharts.com/mapdata/')
        elif jsonp_map:
            self.jsonp_map_flag = True
            self.map = 'geojson'
            self.jsonp_map_url = json.dumps(map_src)
        else:
            self.add_JSsource(map_src)
            map_name = self._get_jsmap_name(map_src)
            self.map = 'geojson'
            self.jsmap = self.map + ' = Highcharts.geojson(' + map_name + ');'
            self.add_JSscript('var ' + self.jsmap, 'head')
        if self.data_temp:
            self.data_temp[0].__options__().update({'mapData': MapObject(self.map)})

    def set_options(self, option_type, option_dict, force_options=False):
        """set plot options"""
        if force_options:
            self.options[option_type].update(option_dict)
        else:
            if option_type == 'yAxis' or option_type == 'xAxis':
                if isinstance(option_dict, list):
                    self.options[option_type] = MultiAxis(option_type)
                    for each_dict in option_dict:
                        (self.options[option_type].update)(**each_dict)

            elif option_type == 'colors':
                self.options['colors'].set_colors(option_dict)
            else:
                if option_type == 'colorAxis':
                    self.options.update({'colorAxis': self.options.get('colorAxis', ColorAxisOptions())})
                    (self.options[option_type].update_dict)(**option_dict)
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

    def _get_jsmap_name(self, url):
        """return 'name' of the map in .js format"""
        ret = urlopen(url)
        return ret.read().decode('utf-8').split('=')[0].replace(' ', '')

    def buildcontent(self):
        """build HTML content only, no header or body tags"""
        self.buildcontainer()
        self.option = json.dumps((self.options), cls=HighchartsEncoder)
        self.setoption = json.dumps((self.setOptions), cls=HighchartsEncoder)
        self.data = json.dumps((self.data_temp), cls=HighchartsEncoder)
        if self.drilldown_flag:
            self.drilldown_data = json.dumps((self.drilldown_data_temp), cls=HighchartsEncoder)
        self._htmlcontent = self.template_content_highcharts.render(chart=self).encode('utf-8')

    def buildhtml(self):
        """Build the HTML page
        Create the htmlheader with css / js
        Create html page
        """
        self.buildcontent()
        self.buildhtmlheader()
        self.content = self._htmlcontent.decode('utf-8')
        self._htmlcontent = self.template_page_highcharts.render(chart=self)
        return self._htmlcontent

    def buildhtmlheader(self):
        """generate HTML header content"""
        if self.drilldown_flag:
            self.add_JSsource('https://code.highcharts.com/maps/modules/drilldown.js')
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

    def save_file(self, filename='Map'):
        """ save htmlcontent as .html file """
        filename = filename + '.html'
        with open(filename, 'w') as (f):
            f.write(self.htmlcontent)
        f.closed


class HighchartsEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        (json.JSONEncoder.__init__)(self, *args, **kwargs)
        self._replacement_map = {}

    def default--- This code section failed: ---

 L. 462         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              RawJavaScriptText
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    38  'to 38'

 L. 463        10  LOAD_GLOBAL              uuid
               12  LOAD_METHOD              uuid4
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  LOAD_ATTR                hex
               18  STORE_FAST               'key'

 L. 464        20  LOAD_FAST                'obj'
               22  LOAD_METHOD              get_jstext
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _replacement_map
               30  LOAD_FAST                'key'
               32  STORE_SUBSCR     

 L. 465        34  LOAD_FAST                'key'
               36  RETURN_VALUE     
             38_0  COME_FROM             8  '8'

 L. 466        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'obj'
               42  LOAD_GLOBAL              datetime
               44  LOAD_ATTR                datetime
               46  CALL_FUNCTION_2       2  '2 positional arguments'
               48  POP_JUMP_IF_FALSE   124  'to 124'

 L. 467        50  LOAD_FAST                'obj'
               52  LOAD_METHOD              utctimetuple
               54  CALL_METHOD_0         0  '0 positional arguments'
               56  STORE_FAST               'utc'

 L. 468        58  LOAD_STR                 'Date.UTC({year},{month},{day},{hours},{minutes},{seconds},{millisec})'
               60  LOAD_ATTR                format

 L. 469        62  LOAD_FAST                'utc'
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'utc'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  LOAD_CONST               1
               76  BINARY_SUBTRACT  
               78  LOAD_FAST                'utc'
               80  LOAD_CONST               2
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'utc'
               86  LOAD_CONST               3
               88  BINARY_SUBSCR    

 L. 470        90  LOAD_FAST                'utc'
               92  LOAD_CONST               4
               94  BINARY_SUBSCR    
               96  LOAD_FAST                'utc'
               98  LOAD_CONST               5
              100  BINARY_SUBSCR    
              102  LOAD_FAST                'obj'
              104  LOAD_ATTR                microsecond
              106  LOAD_CONST               1000
              108  BINARY_TRUE_DIVIDE
              110  LOAD_CONST               ('year', 'month', 'day', 'hours', 'minutes', 'seconds', 'millisec')
              112  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              114  STORE_FAST               'obj'

 L. 471       116  LOAD_GLOBAL              RawJavaScriptText
              118  LOAD_FAST                'obj'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  RETURN_VALUE     
            124_0  COME_FROM            48  '48'

 L. 472       124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'obj'
              128  LOAD_GLOBAL              BaseOptions
              130  CALL_FUNCTION_2       2  '2 positional arguments'
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L. 473       134  LOAD_FAST                'obj'
              136  LOAD_METHOD              __jsonable__
              138  CALL_METHOD_0         0  '0 positional arguments'
              140  RETURN_VALUE     
            142_0  COME_FROM           132  '132'

 L. 474       142  LOAD_GLOBAL              isinstance
              144  LOAD_FAST                'obj'
              146  LOAD_GLOBAL              CSSObject
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  POP_JUMP_IF_TRUE    182  'to 182'
              152  LOAD_GLOBAL              isinstance
              154  LOAD_FAST                'obj'
              156  LOAD_GLOBAL              Formatter
              158  CALL_FUNCTION_2       2  '2 positional arguments'
              160  POP_JUMP_IF_TRUE    182  'to 182'
              162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'obj'
              166  LOAD_GLOBAL              JSfunction
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  POP_JUMP_IF_TRUE    182  'to 182'

 L. 475       172  LOAD_GLOBAL              isinstance
              174  LOAD_FAST                'obj'
              176  LOAD_GLOBAL              MapObject
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  POP_JUMP_IF_FALSE   190  'to 190'
            182_0  COME_FROM           170  '170'
            182_1  COME_FROM           160  '160'
            182_2  COME_FROM           150  '150'

 L. 476       182  LOAD_FAST                'obj'
              184  LOAD_METHOD              __jsonable__
              186  CALL_METHOD_0         0  '0 positional arguments'
              188  RETURN_VALUE     
            190_0  COME_FROM           180  '180'

 L. 477       190  LOAD_GLOBAL              isinstance
              192  LOAD_FAST                'obj'
              194  LOAD_GLOBAL              SeriesOptions
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  POP_JUMP_IF_TRUE    210  'to 210'
              200  LOAD_GLOBAL              isinstance
              202  LOAD_FAST                'obj'
              204  LOAD_GLOBAL              Series
              206  CALL_FUNCTION_2       2  '2 positional arguments'
              208  POP_JUMP_IF_FALSE   218  'to 218'
            210_0  COME_FROM           198  '198'

 L. 478       210  LOAD_FAST                'obj'
              212  LOAD_METHOD              __jsonable__
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  RETURN_VALUE     
            218_0  COME_FROM           208  '208'

 L. 479       218  LOAD_GLOBAL              isinstance
              220  LOAD_FAST                'obj'
              222  LOAD_GLOBAL              CommonObject
              224  CALL_FUNCTION_2       2  '2 positional arguments'
          226_228  POP_JUMP_IF_TRUE    254  'to 254'
              230  LOAD_GLOBAL              isinstance
              232  LOAD_FAST                'obj'
              234  LOAD_GLOBAL              ArrayObject
              236  CALL_FUNCTION_2       2  '2 positional arguments'
          238_240  POP_JUMP_IF_TRUE    254  'to 254'
              242  LOAD_GLOBAL              isinstance
              244  LOAD_FAST                'obj'
              246  LOAD_GLOBAL              ColorObject
              248  CALL_FUNCTION_2       2  '2 positional arguments'
          250_252  POP_JUMP_IF_FALSE   262  'to 262'
            254_0  COME_FROM           238  '238'
            254_1  COME_FROM           226  '226'

 L. 480       254  LOAD_FAST                'obj'
              256  LOAD_METHOD              __jsonable__
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  RETURN_VALUE     
            262_0  COME_FROM           250  '250'

 L. 482       262  LOAD_GLOBAL              json
              264  LOAD_ATTR                JSONEncoder
              266  LOAD_METHOD              default
              268  LOAD_FAST                'self'
              270  LOAD_FAST                'obj'
              272  CALL_METHOD_2         2  '2 positional arguments'
              274  RETURN_VALUE     

Parse error at or near `CALL_METHOD_2' instruction at offset 272

    def encode(self, obj):
        result = json.JSONEncoder.encode(self, obj)
        for k, v in self._replacement_map.items():
            result = result.replace('"%s"' % (k,), v)

        return result


class OptionTypeError(Exception):

    def __init__(self, *args):
        self.args = args