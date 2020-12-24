# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\highcharts\highcharts\highchart_types.py
# Compiled at: 2019-06-05 03:25:47
# Size of source mod 2**32: 23655 bytes
from past.builtins import basestring
import json, datetime
from .common import Formatter, Events, Position, ContextButton, Options3d, ResetZoomButton, DrillUpButton, Labels, Marker, Point, PlotBands, States, Tooltip, Title, Zones, Levels, JSfunction, ColorObject, CSSObject, SVGObject, CommonObject, ArrayObject
PLOT_OPTION_ALLOWED_ARGS = {'common':{'animation':bool, 
  'color':(
   ColorObject, basestring, dict), 
  'cursor':basestring, 
  'dataLabels':(
   Labels, dict), 
  'enableMouseTracking':bool, 
  'events':(
   Events, dict), 
  'id':basestring, 
  'index':[
   float, int], 
  'name':basestring, 
  'point':(
   Point, dict), 
  'selected':bool, 
  'showCheckbox':bool, 
  'showInLegend':bool, 
  'states':(
   States, dict), 
  'stickyTracking':bool, 
  'tooltip':(
   Tooltip, dict), 
  'visible':bool, 
  'xAxis':[
   int, basestring], 
  'yAxis':[
   int, basestring], 
  'zIndex':int, 
  'zoneAxis':basestring, 
  'zones':(
   Zones, dict)}, 
 'area':{'allowPointSelect':bool, 
  'connectEnds':bool, 
  'connectNulls':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'fillColor':(
   ColorObject, basestring, dict), 
  'fillOpacity':float, 
  'getExtremesFromAll':bool, 
  'keys':list, 
  'legendIndex':[
   int, float], 
  'lineColor':(
   ColorObject, basestring, dict), 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'marker':(
   Marker, dict), 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'negativeFillColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':(
   int, basestring, datetime.datetime), 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'step':bool, 
  'threshold':[
   int, type(None)], 
  'trackByArea':bool, 
  'turboThreshold':int}, 
 'arearange':{'allowPointSelect':bool, 
  'connectNulls':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'fillColor':(
   ColorObject, basestring, dict), 
  'fillOpacity':float, 
  'getExtremesFromAll':bool, 
  'keys':list, 
  'legendIndex':[
   int, float], 
  'lineColor':(
   ColorObject, basestring, dict), 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'negativeFillColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'trackByArea':bool, 
  'turboThreshold':int}, 
 'areaspline':{'allowPointSelect':bool, 
  'cropThreshold':int, 
  'connectEnds':bool, 
  'connectNulls':bool, 
  'dashStyle':basestring, 
  'fillColor':(
   ColorObject, basestring, dict), 
  'fillOpacity':float, 
  'getExtremesFromAll':bool, 
  'keys':list, 
  'legendIndex':[
   int, float], 
  'lineColor':(
   ColorObject, basestring, dict), 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'marker':(
   Marker, dict), 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'negativeFillColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'stack':basestring, 
  'stacking':basestring, 
  'threshold':[
   int, type(None)], 
  'turboThreshold':int, 
  'trackByArea':bool}, 
 'areasplinerange':{'allowPointSelect':bool, 
  'connectNulls':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'fillColor':(
   ColorObject, basestring, dict), 
  'fillOpacity':float, 
  'lineColor':(
   ColorObject, basestring, dict), 
  'lineWidth':int, 
  'pointInterval':int, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'turboThreshold':int, 
  'trackByArea':bool}, 
 'bar':{'allowPointSelect':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderRadius':int, 
  'borderWidth':[
   int, basestring], 
  'colorByPoint':bool, 
  'colors':list, 
  'cropThreshold':int, 
  'depth':[
   int, float], 
  'edgeColor':(
   ColorObject, basestring, dict), 
  'edgeWidth':int, 
  'getExtremesFromAll':bool, 
  'groupPadding':[
   float, int], 
  'groupZPadding':[
   float, int], 
  'grouping':bool, 
  'keys':list, 
  'linkedTo':basestring, 
  'minPointLength':int, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPadding':[
   float, int], 
  'pointPlacement':[
   basestring, int, float], 
  'pointRange':int, 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'pointWidth':int, 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'threshold':[
   int, type(None)], 
  'turboThreshold':int}, 
 'boxplot':{'allowPointSelect':bool, 
  'colorByPoint':bool, 
  'colors':list, 
  'depth':[
   int, float], 
  'edgeColor':(
   ColorObject, basestring, dict), 
  'edgeWidth':int, 
  'fillColor':(
   ColorObject, basestring, dict), 
  'getExtremesFromAll':bool, 
  'groupPadding':[
   float, int], 
  'groupZPadding':[
   float, int], 
  'grouping':bool, 
  'keys':list, 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'medianColor':(
   ColorObject, basestring, dict), 
  'medianWidth':[
   int, float], 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPadding':[
   float, int], 
  'pointPlacement':[
   basestring, int, float], 
  'pointRange':int, 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'pointWidth':int, 
  'shadow':[
   bool, dict], 
  'size':[
   int, basestring], 
  'slicedOffset':int, 
  'startAngle':int, 
  'showInLegend':bool}, 
 'bubble':{'allowPointSelect':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderRadius':int, 
  'borderWidth':int, 
  'colors':list, 
  'colorByPoint':bool, 
  'cropThreshold':int, 
  'depth':[
   int, float], 
  'edgeColor':(
   ColorObject, basestring, dict), 
  'edgeWidth':int, 
  'getExtremesFromAll':bool, 
  'groupPadding':[
   float, int], 
  'groupZPadding':[
   float, int], 
  'grouping':bool, 
  'keys':list, 
  'linkedTo':basestring, 
  'minPointLength':int, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPadding':[
   float, int], 
  'pointPlacement':[
   basestring, int, float], 
  'pointRange':int, 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'pointWidth':int, 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'threshold':[
   int, type(None)], 
  'turboThreshold':int}, 
 'column':{'allowPointSelect':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderRadius':int, 
  'borderWidth':[
   int, basestring], 
  'colors':list, 
  'colorByPoint':bool, 
  'cropThreshold':int, 
  'depth':[
   int, float], 
  'edgeColor':(
   ColorObject, basestring, dict), 
  'edgeWidth':int, 
  'getExtremesFromAll':bool, 
  'groupPadding':[
   float, int], 
  'groupZPadding':[
   float, int], 
  'grouping':bool, 
  'keys':list, 
  'linkedTo':basestring, 
  'lineColor':(
   ColorObject, basestring, dict), 
  'lineWidth':int, 
  'minPointLength':int, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointPadding':[
   float, int], 
  'pointRange':int, 
  'pointWidth':[
   int, float], 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'threshold':[
   int, type(None)], 
  'turboThreshold':int}, 
 'columnrange':{'allowPointSelect':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderRadius':int, 
  'borderWidth':[
   int, basestring], 
  'colors':list, 
  'colorByPoint':bool, 
  'depth':[
   int, float], 
  'edgeColor':(
   ColorObject, basestring, dict), 
  'edgeWidth':int, 
  'getExtremesFromAll':bool, 
  'cropThreshold':int, 
  'groupPadding':[
   float, int], 
  'groupZPadding':[
   float, int], 
  'grouping':bool, 
  'keys':list, 
  'linkedTo':basestring, 
  'lineColor':(
   ColorObject, basestring, dict), 
  'lineWidth':int, 
  'minPointLength':int, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointPadding':[
   float, int], 
  'pointRange':int, 
  'pointWidth':int, 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'threshold':[
   int, type(None)], 
  'turboThreshold':int}, 
 'errorbar':{'allowPointSelect':bool, 
  'colors':list, 
  'colorByPoint':bool, 
  'cursor':basestring, 
  'depth':[
   int, float], 
  'edgeColor':(
   ColorObject, basestring, dict), 
  'edgeWidth':int, 
  'getExtremesFromAll':bool, 
  'cropThreshold':int, 
  'groupZPadding':[
   float, int], 
  'keys':list, 
  'linkedTo':basestring, 
  'lineWidth':int, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointPadding':[
   float, int], 
  'pointRange':int, 
  'pointWidth':int, 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'stemColor':(
   ColorObject, basestring, dict), 
  'stemDashStyle':basestring, 
  'stemWidth':[
   float, int], 
  'stickyTracking':bool, 
  'turboThreshold':int, 
  'whiskerColor':(
   ColorObject, basestring, dict), 
  'whiskerLength':[
   float, int, basestring], 
  'whiskerWidth':[
   float, int]}, 
 'gauge':{'dial':NotImplemented, 
  'linkedTo':basestring, 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'overshoot':[
   int, float], 
  'pivot':NotImplemented, 
  'stickyTracking':bool, 
  'threshold':[
   int, type(None)], 
  'wrap':bool}, 
 'heatmap':{'allowPointSelect':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderRadius':int, 
  'borderWidth':[
   int, basestring], 
  'colors':list, 
  'colorByPoint':bool, 
  'colsize':int, 
  'cropThreshold':int, 
  'getExtremesFromAll':bool, 
  'keys':list, 
  'legendIndex':[
   int, float], 
  'linkedTo':basestring, 
  'rowsize':int, 
  'shadow':[
   bool, dict], 
  'stickyTracking':bool, 
  'turboThreshold':int}, 
 'line':{'allowPointSelect':bool, 
  'connectEnds':bool, 
  'connectNulls':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'getExtremesFromAll':bool, 
  'keys':list, 
  'legendIndex':[
   int, float], 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'marker':(
   Marker, dict), 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'stack':basestring, 
  'stacking':basestring, 
  'step':basestring, 
  'turboThreshold':int}, 
 'pie':{'allowPointSelect':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderWidth':[
   int, basestring], 
  'center':list, 
  'colors':list, 
  'depth':[
   int, float], 
  'endAngle':[
   int, float], 
  'ignoreHiddenPoint':bool, 
  'innerSize':[
   int, basestring], 
  'legendIndex':[
   int, basestring], 
  'linkedTo':basestring, 
  'minSize':[
   int, basestring], 
  'shadow':[
   bool, dict], 
  'showInLegend':bool, 
  'size':[
   int, basestring], 
  'slicedOffset':int, 
  'startAngle':int}, 
 'scatter':{'allowPointSelect':bool, 
  'colorByPoint':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'keys':list, 
  'legendIndex':[
   int, float], 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'marker':(
   Marker, dict), 
  'negativeColor':(
   ColorObject, basestring, dict), 
  'pointInterval':int, 
  'pointIntervalUnit':basestring, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'threshold':[
   int, float], 
  'turboThreshold':int}, 
 'series':{'allowPointSelect':bool, 
  'borderWidth':[
   int, basestring], 
  'connectEnds':bool, 
  'connectNulls':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'lineWidth':int, 
  'marker':(
   Marker, dict), 
  'pointInterval':int, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'turboThreshold':int}, 
 'spline':{'allowPointSelect':bool, 
  'connectEnds':bool, 
  'connectNulls':bool, 
  'cropThreshold':int, 
  'dashStyle':basestring, 
  'lineWidth':int, 
  'linkedTo':basestring, 
  'marker':(
   Marker, dict), 
  'pointInterval':int, 
  'pointPlacement':[
   basestring, int, float], 
  'pointStart':[
   int, basestring, datetime.datetime], 
  'shadow':[
   bool, dict], 
  'stacking':basestring, 
  'turboThreshold':int}, 
 'treemap':{'allowDrillToNode':bool, 
  'allowPointSelect':bool, 
  'alternateStartingDirection':bool, 
  'borderColor':(
   ColorObject, basestring, dict), 
  'borderWidth':[
   int, basestring], 
  'colors':list, 
  'colorByPoint':bool, 
  'cropThreshold':int, 
  'getExtremesFromAll':bool, 
  'interactByLeaf':bool, 
  'keys':list, 
  'layoutAlgorithm':basestring, 
  'layoutStartingDirection':basestring, 
  'legendIndex':[
   int, float], 
  'levelIsConstant':bool, 
  'levels':(
   Levels, dict, list), 
  'linkedTo':basestring, 
  'shadow':[
   bool, dict], 
  'stickyTracking':bool, 
  'turboThreshold':int}}
DATA_SERIES_ALLOWED_OPTIONS = {'color':(
  ColorObject, basestring, dict), 
 'connectEnds':bool, 
 'connectNulls':bool, 
 'dataLabels':(
  Labels, dict), 
 'dataParser':NotImplemented, 
 'dataURL':NotImplemented, 
 'drilldown':basestring, 
 'events':(
  Events, dict), 
 'high':[
  int, float], 
 'id':basestring, 
 'index':int, 
 'legendIndex':int, 
 'name':basestring, 
 'marker':(
  Marker, dict), 
 'selected':bool, 
 'sliced':bool, 
 'showInLegend':bool, 
 'stack':basestring, 
 'type':basestring, 
 'visible':bool, 
 'x':[
  int, float], 
 'xAxis':int, 
 'yAxis':int}
DEFAULT_OPTIONS = {}

class OptionTypeError(Exception):

    def __init__(self, *args):
        self.args = args


class SeriesOptions(object):
    __doc__ = 'Class for plotOptions'

    def __init__(self, series_type='line', supress_errors=False, **kwargs):
        self.load_defaults(series_type)
        self.process_kwargs(kwargs, series_type=series_type, supress_errors=supress_errors)

    @staticmethod
    def __validate_options__(k, v, ov):
        if isinstance(ov, list):
            if isinstance(v, tuple(ov)):
                return True
            raise OptionTypeError('Option Type Currently Not Supported: %s' % k)
        else:
            if ov == NotImplemented:
                raise OptionTypeError('Option Type Currently Not Supported: %s' % k)
            if isinstance(v, ov):
                return True
            return False

    def __options__(self):
        return self.__dict__

    def __jsonable__(self):
        return self.__dict__

    def update--- This code section failed: ---

 L. 526         0  LOAD_GLOBAL              PLOT_OPTION_ALLOWED_ARGS
                2  LOAD_FAST                'series_type'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'allowed_args'

 L. 527         8  LOAD_FAST                'allowed_args'
               10  LOAD_METHOD              update
               12  LOAD_GLOBAL              PLOT_OPTION_ALLOWED_ARGS
               14  LOAD_STR                 'common'
               16  BINARY_SUBSCR    
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_TOP          

 L. 528     22_24  SETUP_LOOP          818  'to 818'
               26  LOAD_FAST                'kwargs'
               28  LOAD_METHOD              items
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  GET_ITER         
             34_0  COME_FROM           796  '796'
            34_36  FOR_ITER            816  'to 816'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'k'
               42  STORE_FAST               'v'

 L. 529        44  LOAD_FAST                'k'
               46  LOAD_FAST                'allowed_args'
               48  COMPARE_OP               in
            50_52  POP_JUMP_IF_FALSE   784  'to 784'

 L. 530        54  LOAD_GLOBAL              SeriesOptions
               56  LOAD_METHOD              __validate_options__
               58  LOAD_FAST                'k'
               60  LOAD_FAST                'v'
               62  LOAD_FAST                'allowed_args'
               64  LOAD_FAST                'k'
               66  BINARY_SUBSCR    
               68  CALL_METHOD_3         3  '3 positional arguments'
            70_72  POP_JUMP_IF_FALSE   814  'to 814'

 L. 531        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'allowed_args'
               78  LOAD_FAST                'k'
               80  BINARY_SUBSCR    
               82  LOAD_GLOBAL              tuple
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  POP_JUMP_IF_FALSE   208  'to 208'
               88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'allowed_args'
               92  LOAD_FAST                'k'
               94  BINARY_SUBSCR    
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  CALL_FUNCTION_0       0  '0 positional arguments'
              102  LOAD_GLOBAL              CommonObject
              104  CALL_FUNCTION_2       2  '2 positional arguments'
              106  POP_JUMP_IF_FALSE   208  'to 208'

 L. 533       108  LOAD_FAST                'self'
              110  LOAD_METHOD              __getattr__
              112  LOAD_FAST                'k'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_JUMP_IF_FALSE   172  'to 172'

 L. 534       118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'v'
              122  LOAD_GLOBAL              dict
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_JUMP_IF_FALSE   148  'to 148'

 L. 535       128  LOAD_FAST                'self'
              130  LOAD_METHOD              __options__
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  LOAD_FAST                'k'
              136  BINARY_SUBSCR    
              138  LOAD_METHOD              update
              140  LOAD_FAST                'v'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_TOP          
              146  JUMP_ABSOLUTE       204  'to 204'
            148_0  COME_FROM           126  '126'

 L. 537       148  LOAD_FAST                'self'
              150  LOAD_METHOD              __options__
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  LOAD_FAST                'k'
              156  BINARY_SUBSCR    
              158  LOAD_METHOD              __options__
              160  CALL_METHOD_0         0  '0 positional arguments'
              162  LOAD_METHOD              update
              164  LOAD_FAST                'v'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_TOP          
              170  JUMP_ABSOLUTE       814  'to 814'
            172_0  COME_FROM           116  '116'

 L. 539       172  LOAD_FAST                'self'
              174  LOAD_METHOD              __options__
              176  CALL_METHOD_0         0  '0 positional arguments'
              178  LOAD_METHOD              update
              180  LOAD_FAST                'k'
              182  LOAD_FAST                'allowed_args'
              184  LOAD_FAST                'k'
              186  BINARY_SUBSCR    
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  BUILD_TUPLE_0         0 
              194  LOAD_FAST                'v'
              196  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              198  BUILD_MAP_1           1 
              200  CALL_METHOD_1         1  '1 positional argument'
              202  POP_TOP          
          204_206  JUMP_ABSOLUTE       814  'to 814'
            208_0  COME_FROM           106  '106'
            208_1  COME_FROM            86  '86'

 L. 541       208  LOAD_GLOBAL              isinstance
              210  LOAD_FAST                'allowed_args'
              212  LOAD_FAST                'k'
              214  BINARY_SUBSCR    
              216  LOAD_GLOBAL              tuple
              218  CALL_FUNCTION_2       2  '2 positional arguments'
          220_222  POP_JUMP_IF_FALSE   370  'to 370'
              224  LOAD_GLOBAL              isinstance
              226  LOAD_FAST                'allowed_args'
              228  LOAD_FAST                'k'
              230  BINARY_SUBSCR    
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_0       0  '0 positional arguments'
              238  LOAD_GLOBAL              ArrayObject
              240  CALL_FUNCTION_2       2  '2 positional arguments'
          242_244  POP_JUMP_IF_FALSE   370  'to 370'

 L. 543       246  LOAD_GLOBAL              isinstance
              248  LOAD_FAST                'v'
              250  LOAD_GLOBAL              dict
              252  CALL_FUNCTION_2       2  '2 positional arguments'
          254_256  POP_JUMP_IF_FALSE   290  'to 290'

 L. 544       258  LOAD_FAST                'self'
              260  LOAD_ATTR                __dict__
              262  LOAD_FAST                'k'
              264  BINARY_SUBSCR    
              266  LOAD_METHOD              append
              268  LOAD_FAST                'allowed_args'
              270  LOAD_FAST                'k'
              272  BINARY_SUBSCR    
              274  LOAD_CONST               0
              276  BINARY_SUBSCR    
              278  BUILD_TUPLE_0         0 
              280  LOAD_FAST                'v'
              282  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              284  CALL_METHOD_1         1  '1 positional argument'
              286  POP_TOP          
              288  JUMP_ABSOLUTE       814  'to 814'
            290_0  COME_FROM           254  '254'

 L. 545       290  LOAD_GLOBAL              isinstance
              292  LOAD_FAST                'v'
              294  LOAD_GLOBAL              list
              296  CALL_FUNCTION_2       2  '2 positional arguments'
          298_300  POP_JUMP_IF_FALSE   350  'to 350'

 L. 546       302  SETUP_LOOP          366  'to 366'
              304  LOAD_FAST                'v'
              306  GET_ITER         
              308  FOR_ITER            346  'to 346'
              310  STORE_FAST               'item'

 L. 547       312  LOAD_FAST                'self'
              314  LOAD_ATTR                __dict__
              316  LOAD_FAST                'k'
              318  BINARY_SUBSCR    
              320  LOAD_METHOD              append
              322  LOAD_FAST                'allowed_args'
              324  LOAD_FAST                'k'
              326  BINARY_SUBSCR    
              328  LOAD_CONST               0
              330  BINARY_SUBSCR    
              332  BUILD_TUPLE_0         0 
              334  LOAD_FAST                'item'
              336  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              338  CALL_METHOD_1         1  '1 positional argument'
              340  POP_TOP          
          342_344  JUMP_BACK           308  'to 308'
              346  POP_BLOCK        
              348  JUMP_ABSOLUTE       814  'to 814'
            350_0  COME_FROM           298  '298'

 L. 549       350  LOAD_GLOBAL              OptionTypeError
              352  LOAD_STR                 'Not An Accepted Input Type: %s'
              354  LOAD_GLOBAL              type
              356  LOAD_FAST                'v'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  BINARY_MODULO    
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  POP_TOP          
            366_0  COME_FROM_LOOP      302  '302'
          366_368  JUMP_ABSOLUTE       814  'to 814'
            370_0  COME_FROM           242  '242'
            370_1  COME_FROM           220  '220'

 L. 551       370  LOAD_GLOBAL              isinstance
              372  LOAD_FAST                'allowed_args'
              374  LOAD_FAST                'k'
              376  BINARY_SUBSCR    
              378  LOAD_GLOBAL              tuple
              380  CALL_FUNCTION_2       2  '2 positional arguments'
          382_384  POP_JUMP_IF_FALSE   610  'to 610'

 L. 552       386  LOAD_GLOBAL              isinstance
              388  LOAD_FAST                'allowed_args'
              390  LOAD_FAST                'k'
              392  BINARY_SUBSCR    
              394  LOAD_CONST               0
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_0       0  '0 positional arguments'
              400  LOAD_GLOBAL              CSSObject
              402  CALL_FUNCTION_2       2  '2 positional arguments'
          404_406  POP_JUMP_IF_TRUE    430  'to 430'
              408  LOAD_GLOBAL              isinstance
              410  LOAD_FAST                'allowed_args'
              412  LOAD_FAST                'k'
              414  BINARY_SUBSCR    
              416  LOAD_CONST               0
              418  BINARY_SUBSCR    
              420  CALL_FUNCTION_0       0  '0 positional arguments'
              422  LOAD_GLOBAL              SVGObject
              424  CALL_FUNCTION_2       2  '2 positional arguments'
          426_428  POP_JUMP_IF_FALSE   610  'to 610'
            430_0  COME_FROM           404  '404'

 L. 553       430  LOAD_FAST                'self'
              432  LOAD_METHOD              __getattr__
              434  LOAD_FAST                'k'
              436  CALL_METHOD_1         1  '1 positional argument'
          438_440  POP_JUMP_IF_FALSE   492  'to 492'

 L. 554       442  SETUP_LOOP          522  'to 522'
              444  LOAD_FAST                'v'
              446  LOAD_METHOD              items
              448  CALL_METHOD_0         0  '0 positional arguments'
              450  GET_ITER         
              452  FOR_ITER            488  'to 488'
              454  UNPACK_SEQUENCE_2     2 
              456  STORE_FAST               'key'
              458  STORE_FAST               'value'

 L. 555       460  LOAD_FAST                'self'
              462  LOAD_ATTR                __dict__
              464  LOAD_FAST                'k'
              466  BINARY_SUBSCR    
              468  LOAD_METHOD              __options__
              470  CALL_METHOD_0         0  '0 positional arguments'
              472  LOAD_METHOD              update
              474  LOAD_FAST                'key'
              476  LOAD_FAST                'value'
              478  BUILD_MAP_1           1 
              480  CALL_METHOD_1         1  '1 positional argument'
              482  POP_TOP          
          484_486  JUMP_BACK           452  'to 452'
              488  POP_BLOCK        
              490  JUMP_FORWARD        522  'to 522'
            492_0  COME_FROM           438  '438'

 L. 557       492  LOAD_FAST                'self'
              494  LOAD_ATTR                __dict__
              496  LOAD_METHOD              update
              498  LOAD_FAST                'k'
              500  LOAD_FAST                'allowed_args'
              502  LOAD_FAST                'k'
              504  BINARY_SUBSCR    
              506  LOAD_CONST               0
              508  BINARY_SUBSCR    
              510  BUILD_TUPLE_0         0 
              512  LOAD_FAST                'v'
              514  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              516  BUILD_MAP_1           1 
              518  CALL_METHOD_1         1  '1 positional argument'
              520  POP_TOP          
            522_0  COME_FROM           490  '490'
            522_1  COME_FROM_LOOP      442  '442'

 L. 559       522  LOAD_FAST                'self'
              524  LOAD_ATTR                __dict__
              526  LOAD_FAST                'k'
              528  BINARY_SUBSCR    
              530  LOAD_METHOD              __options__
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  STORE_FAST               'v'

 L. 561       536  LOAD_GLOBAL              isinstance
              538  LOAD_FAST                'v'
              540  LOAD_GLOBAL              dict
              542  CALL_FUNCTION_2       2  '2 positional arguments'
          544_546  POP_JUMP_IF_FALSE   580  'to 580'

 L. 562       548  LOAD_FAST                'self'
              550  LOAD_ATTR                __dict__
              552  LOAD_METHOD              update
              554  LOAD_FAST                'k'
              556  LOAD_FAST                'allowed_args'
              558  LOAD_FAST                'k'
              560  BINARY_SUBSCR    
              562  LOAD_CONST               0
              564  BINARY_SUBSCR    
              566  BUILD_TUPLE_0         0 
              568  LOAD_FAST                'v'
              570  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              572  BUILD_MAP_1           1 
              574  CALL_METHOD_1         1  '1 positional argument'
              576  POP_TOP          
              578  JUMP_FORWARD        608  'to 608'
            580_0  COME_FROM           544  '544'

 L. 564       580  LOAD_FAST                'self'
              582  LOAD_ATTR                __dict__
              584  LOAD_METHOD              update
              586  LOAD_FAST                'k'
              588  LOAD_FAST                'allowed_args'
              590  LOAD_FAST                'k'
              592  BINARY_SUBSCR    
              594  LOAD_CONST               0
              596  BINARY_SUBSCR    
              598  LOAD_FAST                'v'
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  BUILD_MAP_1           1 
              604  CALL_METHOD_1         1  '1 positional argument'
              606  POP_TOP          
            608_0  COME_FROM           578  '578'
              608  JUMP_FORWARD        782  'to 782'
            610_0  COME_FROM           426  '426'
            610_1  COME_FROM           382  '382'

 L. 566       610  LOAD_GLOBAL              isinstance
              612  LOAD_FAST                'allowed_args'
              614  LOAD_FAST                'k'
              616  BINARY_SUBSCR    
              618  LOAD_GLOBAL              tuple
              620  CALL_FUNCTION_2       2  '2 positional arguments'
          622_624  POP_JUMP_IF_FALSE   766  'to 766'
              626  LOAD_GLOBAL              isinstance
              628  LOAD_FAST                'allowed_args'
              630  LOAD_FAST                'k'
              632  BINARY_SUBSCR    
              634  LOAD_CONST               0
              636  BINARY_SUBSCR    
              638  CALL_FUNCTION_0       0  '0 positional arguments'
              640  LOAD_GLOBAL              JSfunction
              642  CALL_FUNCTION_2       2  '2 positional arguments'
          644_646  POP_JUMP_IF_TRUE    692  'to 692'

 L. 567       648  LOAD_GLOBAL              isinstance
              650  LOAD_FAST                'allowed_args'
              652  LOAD_FAST                'k'
              654  BINARY_SUBSCR    
              656  LOAD_CONST               0
              658  BINARY_SUBSCR    
              660  CALL_FUNCTION_0       0  '0 positional arguments'
              662  LOAD_GLOBAL              Formatter
              664  CALL_FUNCTION_2       2  '2 positional arguments'
          666_668  POP_JUMP_IF_TRUE    692  'to 692'
              670  LOAD_GLOBAL              isinstance
              672  LOAD_FAST                'allowed_args'
              674  LOAD_FAST                'k'
              676  BINARY_SUBSCR    
              678  LOAD_CONST               0
              680  BINARY_SUBSCR    
              682  CALL_FUNCTION_0       0  '0 positional arguments'
              684  LOAD_GLOBAL              ColorObject
              686  CALL_FUNCTION_2       2  '2 positional arguments'
          688_690  POP_JUMP_IF_FALSE   766  'to 766'
            692_0  COME_FROM           666  '666'
            692_1  COME_FROM           644  '644'

 L. 568       692  LOAD_GLOBAL              isinstance
              694  LOAD_FAST                'v'
              696  LOAD_GLOBAL              dict
              698  CALL_FUNCTION_2       2  '2 positional arguments'
          700_702  POP_JUMP_IF_FALSE   736  'to 736'

 L. 569       704  LOAD_FAST                'self'
              706  LOAD_ATTR                __dict__
              708  LOAD_METHOD              update
              710  LOAD_FAST                'k'
              712  LOAD_FAST                'allowed_args'
              714  LOAD_FAST                'k'
              716  BINARY_SUBSCR    
              718  LOAD_CONST               0
              720  BINARY_SUBSCR    
              722  BUILD_TUPLE_0         0 
              724  LOAD_FAST                'v'
              726  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              728  BUILD_MAP_1           1 
              730  CALL_METHOD_1         1  '1 positional argument'
              732  POP_TOP          
              734  JUMP_FORWARD        764  'to 764'
            736_0  COME_FROM           700  '700'

 L. 571       736  LOAD_FAST                'self'
              738  LOAD_ATTR                __dict__
              740  LOAD_METHOD              update
              742  LOAD_FAST                'k'
              744  LOAD_FAST                'allowed_args'
              746  LOAD_FAST                'k'
              748  BINARY_SUBSCR    
              750  LOAD_CONST               0
              752  BINARY_SUBSCR    
              754  LOAD_FAST                'v'
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  BUILD_MAP_1           1 
              760  CALL_METHOD_1         1  '1 positional argument'
              762  POP_TOP          
            764_0  COME_FROM           734  '734'
              764  JUMP_FORWARD        782  'to 782'
            766_0  COME_FROM           688  '688'
            766_1  COME_FROM           622  '622'

 L. 573       766  LOAD_FAST                'self'
              768  LOAD_ATTR                __dict__
              770  LOAD_METHOD              update
              772  LOAD_FAST                'k'
              774  LOAD_FAST                'v'
              776  BUILD_MAP_1           1 
              778  CALL_METHOD_1         1  '1 positional argument'
              780  POP_TOP          
            782_0  COME_FROM           764  '764'
            782_1  COME_FROM           608  '608'
              782  JUMP_BACK            34  'to 34'
            784_0  COME_FROM            50  '50'

 L. 575       784  LOAD_GLOBAL              print
              786  LOAD_FAST                'k'
              788  LOAD_FAST                'v'
              790  CALL_FUNCTION_2       2  '2 positional arguments'
              792  POP_TOP          

 L. 576       794  LOAD_GLOBAL              supress_errors
              796  POP_JUMP_IF_TRUE     34  'to 34'

 L. 576       798  LOAD_GLOBAL              OptionTypeError
              800  LOAD_STR                 'Option Type Mismatch: Expected: %s'
              802  LOAD_FAST                'allowed_args'
              804  LOAD_FAST                'k'
              806  BINARY_SUBSCR    
              808  BINARY_MODULO    
              810  CALL_FUNCTION_1       1  '1 positional argument'
              812  RAISE_VARARGS_1       1  'exception instance'
            814_0  COME_FROM            70  '70'
              814  JUMP_BACK            34  'to 34'
              816  POP_BLOCK        
            818_0  COME_FROM_LOOP       22  '22'

Parse error at or near `COME_FROM_LOOP' instruction at offset 366_0

    def process_kwargs--- This code section failed: ---

 L. 580         0  LOAD_GLOBAL              PLOT_OPTION_ALLOWED_ARGS
                2  LOAD_FAST                'series_type'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'allowed_args'

 L. 581         8  LOAD_FAST                'allowed_args'
               10  LOAD_METHOD              update
               12  LOAD_GLOBAL              PLOT_OPTION_ALLOWED_ARGS
               14  LOAD_STR                 'common'
               16  BINARY_SUBSCR    
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_TOP          

 L. 583     22_24  SETUP_LOOP          464  'to 464'
               26  LOAD_FAST                'kwargs'
               28  LOAD_METHOD              items
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  GET_ITER         
             34_0  COME_FROM           442  '442'
             34_1  COME_FROM            50  '50'
            34_36  FOR_ITER            462  'to 462'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'k'
               42  STORE_FAST               'v'

 L. 584        44  LOAD_FAST                'k'
               46  LOAD_FAST                'allowed_args'
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE    34  'to 34'

 L. 585        52  LOAD_GLOBAL              SeriesOptions
               54  LOAD_METHOD              __validate_options__
               56  LOAD_FAST                'k'
               58  LOAD_FAST                'v'
               60  LOAD_FAST                'allowed_args'
               62  LOAD_FAST                'k'
               64  BINARY_SUBSCR    
               66  CALL_METHOD_3         3  '3 positional arguments'
            68_70  POP_JUMP_IF_FALSE   430  'to 430'

 L. 586        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'allowed_args'
               76  LOAD_FAST                'k'
               78  BINARY_SUBSCR    
               80  LOAD_GLOBAL              tuple
               82  CALL_FUNCTION_2       2  '2 positional arguments'
            84_86  POP_JUMP_IF_FALSE   412  'to 412'

 L. 587        88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'v'
               92  LOAD_GLOBAL              dict
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_JUMP_IF_FALSE   132  'to 132'

 L. 588        98  LOAD_FAST                'self'
              100  LOAD_ATTR                __dict__
              102  LOAD_METHOD              update
              104  LOAD_FAST                'k'
              106  LOAD_FAST                'allowed_args'
              108  LOAD_FAST                'k'
              110  BINARY_SUBSCR    
              112  LOAD_CONST               0
              114  BINARY_SUBSCR    
              116  BUILD_TUPLE_0         0 
              118  LOAD_FAST                'v'
              120  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              122  BUILD_MAP_1           1 
              124  CALL_METHOD_1         1  '1 positional argument'
              126  POP_TOP          
          128_130  JUMP_ABSOLUTE       428  'to 428'
            132_0  COME_FROM            96  '96'

 L. 589       132  LOAD_GLOBAL              isinstance
              134  LOAD_FAST                'v'
              136  LOAD_GLOBAL              list
              138  CALL_FUNCTION_2       2  '2 positional arguments'
          140_142  POP_JUMP_IF_FALSE   266  'to 266'

 L. 590       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'v'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  LOAD_CONST               1
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   192  'to 192'

 L. 591       156  LOAD_FAST                'self'
              158  LOAD_ATTR                __dict__
              160  LOAD_METHOD              update
              162  LOAD_FAST                'k'
              164  LOAD_FAST                'allowed_args'
              166  LOAD_FAST                'k'
              168  BINARY_SUBSCR    
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  BUILD_TUPLE_0         0 
              176  LOAD_FAST                'v'
              178  LOAD_CONST               0
              180  BINARY_SUBSCR    
              182  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              184  BUILD_MAP_1           1 
              186  CALL_METHOD_1         1  '1 positional argument'
              188  POP_TOP          
              190  JUMP_FORWARD        264  'to 264'
            192_0  COME_FROM           154  '154'

 L. 593       192  LOAD_FAST                'self'
              194  LOAD_ATTR                __dict__
              196  LOAD_METHOD              update
              198  LOAD_FAST                'k'
              200  LOAD_FAST                'allowed_args'
              202  LOAD_FAST                'k'
              204  BINARY_SUBSCR    
              206  LOAD_CONST               0
              208  BINARY_SUBSCR    
              210  BUILD_TUPLE_0         0 
              212  LOAD_FAST                'v'
              214  LOAD_CONST               0
              216  BINARY_SUBSCR    
              218  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              220  BUILD_MAP_1           1 
              222  CALL_METHOD_1         1  '1 positional argument'
              224  POP_TOP          

 L. 594       226  SETUP_LOOP          410  'to 410'
              228  LOAD_FAST                'v'
              230  LOAD_CONST               1
              232  LOAD_CONST               None
              234  BUILD_SLICE_2         2 
              236  BINARY_SUBSCR    
              238  GET_ITER         
              240  FOR_ITER            262  'to 262'
              242  STORE_FAST               'item'

 L. 595       244  LOAD_FAST                'self'
              246  LOAD_ATTR                __dict__
              248  LOAD_FAST                'k'
              250  BINARY_SUBSCR    
              252  LOAD_METHOD              update
              254  LOAD_FAST                'item'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  POP_TOP          
              260  JUMP_BACK           240  'to 240'
              262  POP_BLOCK        
            264_0  COME_FROM           190  '190'
              264  JUMP_FORWARD        410  'to 410'
            266_0  COME_FROM           140  '140'

 L. 596       266  LOAD_GLOBAL              isinstance
              268  LOAD_FAST                'v'
              270  LOAD_GLOBAL              CommonObject
              272  CALL_FUNCTION_2       2  '2 positional arguments'
          274_276  POP_JUMP_IF_TRUE    364  'to 364'
              278  LOAD_GLOBAL              isinstance
              280  LOAD_FAST                'v'
              282  LOAD_GLOBAL              ArrayObject
              284  CALL_FUNCTION_2       2  '2 positional arguments'
          286_288  POP_JUMP_IF_TRUE    364  'to 364'

 L. 597       290  LOAD_GLOBAL              isinstance
              292  LOAD_FAST                'v'
              294  LOAD_GLOBAL              CSSObject
              296  CALL_FUNCTION_2       2  '2 positional arguments'
          298_300  POP_JUMP_IF_TRUE    364  'to 364'
              302  LOAD_GLOBAL              isinstance
              304  LOAD_FAST                'v'
              306  LOAD_GLOBAL              SVGObject
              308  CALL_FUNCTION_2       2  '2 positional arguments'
          310_312  POP_JUMP_IF_TRUE    364  'to 364'
              314  LOAD_GLOBAL              isinstance
              316  LOAD_FAST                'v'
              318  LOAD_GLOBAL              ColorObject
              320  CALL_FUNCTION_2       2  '2 positional arguments'
          322_324  POP_JUMP_IF_TRUE    364  'to 364'

 L. 598       326  LOAD_GLOBAL              isinstance
              328  LOAD_FAST                'v'
              330  LOAD_GLOBAL              JSfunction
              332  CALL_FUNCTION_2       2  '2 positional arguments'
          334_336  POP_JUMP_IF_TRUE    364  'to 364'
              338  LOAD_GLOBAL              isinstance
              340  LOAD_FAST                'v'
              342  LOAD_GLOBAL              Formatter
              344  CALL_FUNCTION_2       2  '2 positional arguments'
          346_348  POP_JUMP_IF_TRUE    364  'to 364'
              350  LOAD_GLOBAL              isinstance
              352  LOAD_FAST                'v'
              354  LOAD_GLOBAL              datetime
              356  LOAD_ATTR                datetime
              358  CALL_FUNCTION_2       2  '2 positional arguments'
          360_362  POP_JUMP_IF_FALSE   382  'to 382'
            364_0  COME_FROM           346  '346'
            364_1  COME_FROM           334  '334'
            364_2  COME_FROM           322  '322'
            364_3  COME_FROM           310  '310'
            364_4  COME_FROM           298  '298'
            364_5  COME_FROM           286  '286'
            364_6  COME_FROM           274  '274'

 L. 599       364  LOAD_FAST                'self'
              366  LOAD_ATTR                __dict__
              368  LOAD_METHOD              update
              370  LOAD_FAST                'k'
              372  LOAD_FAST                'v'
              374  BUILD_MAP_1           1 
              376  CALL_METHOD_1         1  '1 positional argument'
              378  POP_TOP          
              380  JUMP_FORWARD        410  'to 410'
            382_0  COME_FROM           360  '360'

 L. 601       382  LOAD_FAST                'self'
              384  LOAD_ATTR                __dict__
              386  LOAD_METHOD              update
              388  LOAD_FAST                'k'
              390  LOAD_FAST                'allowed_args'
              392  LOAD_FAST                'k'
              394  BINARY_SUBSCR    
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  LOAD_FAST                'v'
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  BUILD_MAP_1           1 
              406  CALL_METHOD_1         1  '1 positional argument'
              408  POP_TOP          
            410_0  COME_FROM           380  '380'
            410_1  COME_FROM           264  '264'
            410_2  COME_FROM_LOOP      226  '226'
              410  JUMP_FORWARD        428  'to 428'
            412_0  COME_FROM            84  '84'

 L. 603       412  LOAD_FAST                'self'
              414  LOAD_ATTR                __dict__
              416  LOAD_METHOD              update
              418  LOAD_FAST                'k'
              420  LOAD_FAST                'v'
              422  BUILD_MAP_1           1 
              424  CALL_METHOD_1         1  '1 positional argument'
              426  POP_TOP          
            428_0  COME_FROM           410  '410'
              428  JUMP_BACK            34  'to 34'
            430_0  COME_FROM            68  '68'

 L. 605       430  LOAD_GLOBAL              print
              432  LOAD_FAST                'k'
              434  LOAD_FAST                'v'
              436  CALL_FUNCTION_2       2  '2 positional arguments'
              438  POP_TOP          

 L. 606       440  LOAD_FAST                'supress_errors'
              442  POP_JUMP_IF_TRUE     34  'to 34'

 L. 606       444  LOAD_GLOBAL              OptionTypeError
              446  LOAD_STR                 'Option Type Mismatch: Expected: %s'
              448  LOAD_FAST                'allowed_args'
              450  LOAD_FAST                'k'
              452  BINARY_SUBSCR    
              454  BINARY_MODULO    
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  RAISE_VARARGS_1       1  'exception instance'
              460  JUMP_BACK            34  'to 34'
              462  POP_BLOCK        
            464_0  COME_FROM_LOOP       22  '22'

Parse error at or near `JUMP_FORWARD' instruction at offset 380

    def load_defaults(self, series_type):
        self.process_kwargs(DEFAULT_OPTIONS.get(series_type, {}), series_type)

    def __getattr__(self, item):
        if item not in self.__dict__:
            return
        return True


class Series(object):
    __doc__ = 'Series class for input data '

    def __init__--- This code section failed: ---

 L. 626         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              list
                6  CALL_FUNCTION_2       2  '2 positional arguments'
             8_10  POP_JUMP_IF_FALSE   284  'to 284'

 L. 627     12_14  SETUP_LOOP          284  'to 284'
               16  LOAD_FAST                'data'
               18  GET_ITER         
             20_0  COME_FROM            34  '34'
            20_22  FOR_ITER            282  'to 282'
               24  STORE_FAST               'item'

 L. 628        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'item'
               30  LOAD_GLOBAL              dict
               32  CALL_FUNCTION_2       2  '2 positional arguments'
               34  POP_JUMP_IF_FALSE    20  'to 20'

 L. 629        36  SETUP_LOOP          280  'to 280'
               38  LOAD_FAST                'item'
               40  LOAD_METHOD              items
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  GET_ITER         
             46_0  COME_FROM            78  '78'
             46_1  COME_FROM            60  '60'
               46  FOR_ITER            278  'to 278'
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'k'
               52  STORE_FAST               'v'

 L. 630        54  LOAD_FAST                'k'
               56  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    46  'to 46'

 L. 631        62  LOAD_GLOBAL              SeriesOptions
               64  LOAD_METHOD              __validate_options__
               66  LOAD_FAST                'k'
               68  LOAD_FAST                'v'
               70  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
               72  LOAD_FAST                'k'
               74  BINARY_SUBSCR    
               76  CALL_METHOD_3         3  '3 positional arguments'
               78  POP_JUMP_IF_FALSE    46  'to 46'

 L. 632        80  LOAD_GLOBAL              isinstance
               82  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
               84  LOAD_FAST                'k'
               86  BINARY_SUBSCR    
               88  LOAD_GLOBAL              tuple
               90  CALL_FUNCTION_2       2  '2 positional arguments'
            92_94  POP_JUMP_IF_FALSE   262  'to 262'

 L. 633        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'v'
              100  LOAD_GLOBAL              dict
              102  CALL_FUNCTION_2       2  '2 positional arguments'
              104  POP_JUMP_IF_FALSE   136  'to 136'

 L. 634       106  LOAD_FAST                'item'
              108  LOAD_METHOD              update
              110  LOAD_FAST                'k'
              112  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              114  LOAD_FAST                'k'
              116  BINARY_SUBSCR    
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  BUILD_TUPLE_0         0 
              124  LOAD_FAST                'v'
              126  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              128  BUILD_MAP_1           1 
              130  CALL_METHOD_1         1  '1 positional argument'
              132  POP_TOP          
              134  JUMP_FORWARD        260  'to 260'
            136_0  COME_FROM           104  '104'

 L. 635       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'v'
              140  LOAD_GLOBAL              CommonObject
              142  CALL_FUNCTION_2       2  '2 positional arguments'
              144  POP_JUMP_IF_TRUE    218  'to 218'
              146  LOAD_GLOBAL              isinstance
              148  LOAD_FAST                'v'
              150  LOAD_GLOBAL              ArrayObject
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  POP_JUMP_IF_TRUE    218  'to 218'

 L. 636       156  LOAD_GLOBAL              isinstance
              158  LOAD_FAST                'v'
              160  LOAD_GLOBAL              CSSObject
              162  CALL_FUNCTION_2       2  '2 positional arguments'
              164  POP_JUMP_IF_TRUE    218  'to 218'
              166  LOAD_GLOBAL              isinstance
              168  LOAD_FAST                'v'
              170  LOAD_GLOBAL              SVGObject
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  POP_JUMP_IF_TRUE    218  'to 218'
              176  LOAD_GLOBAL              isinstance
              178  LOAD_FAST                'v'
              180  LOAD_GLOBAL              ColorObject
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  POP_JUMP_IF_TRUE    218  'to 218'

 L. 637       186  LOAD_GLOBAL              isinstance
              188  LOAD_FAST                'v'
              190  LOAD_GLOBAL              JSfunction
              192  CALL_FUNCTION_2       2  '2 positional arguments'
              194  POP_JUMP_IF_TRUE    218  'to 218'
              196  LOAD_GLOBAL              isinstance
              198  LOAD_FAST                'v'
              200  LOAD_GLOBAL              Formatter
              202  CALL_FUNCTION_2       2  '2 positional arguments'
              204  POP_JUMP_IF_TRUE    218  'to 218'
              206  LOAD_GLOBAL              isinstance
              208  LOAD_FAST                'v'
              210  LOAD_GLOBAL              datetime
              212  LOAD_ATTR                datetime
              214  CALL_FUNCTION_2       2  '2 positional arguments'
              216  POP_JUMP_IF_FALSE   234  'to 234'
            218_0  COME_FROM           204  '204'
            218_1  COME_FROM           194  '194'
            218_2  COME_FROM           184  '184'
            218_3  COME_FROM           174  '174'
            218_4  COME_FROM           164  '164'
            218_5  COME_FROM           154  '154'
            218_6  COME_FROM           144  '144'

 L. 638       218  LOAD_FAST                'item'
              220  LOAD_METHOD              update
              222  LOAD_FAST                'k'
              224  LOAD_FAST                'v'
              226  BUILD_MAP_1           1 
              228  CALL_METHOD_1         1  '1 positional argument'
              230  POP_TOP          
              232  JUMP_FORWARD        260  'to 260'
            234_0  COME_FROM           216  '216'

 L. 640       234  LOAD_FAST                'item'
              236  LOAD_METHOD              update
              238  LOAD_FAST                'k'
              240  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              242  LOAD_FAST                'k'
              244  BINARY_SUBSCR    
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'v'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  BUILD_MAP_1           1 
              256  CALL_METHOD_1         1  '1 positional argument'
              258  POP_TOP          
            260_0  COME_FROM           232  '232'
            260_1  COME_FROM           134  '134'
              260  JUMP_BACK            46  'to 46'
            262_0  COME_FROM            92  '92'

 L. 642       262  LOAD_FAST                'item'
              264  LOAD_METHOD              update
              266  LOAD_FAST                'k'
              268  LOAD_FAST                'v'
              270  BUILD_MAP_1           1 
              272  CALL_METHOD_1         1  '1 positional argument'
              274  POP_TOP          
              276  JUMP_BACK            46  'to 46'
              278  POP_BLOCK        
            280_0  COME_FROM_LOOP       36  '36'
              280  JUMP_BACK            20  'to 20'
              282  POP_BLOCK        
            284_0  COME_FROM_LOOP       12  '12'
            284_1  COME_FROM             8  '8'

 L. 644       284  LOAD_FAST                'self'
              286  LOAD_ATTR                __dict__
              288  LOAD_METHOD              update

 L. 645       290  LOAD_FAST                'data'

 L. 646       292  LOAD_FAST                'series_type'
              294  LOAD_CONST               ('data', 'type')
              296  BUILD_CONST_KEY_MAP_2     2 
              298  CALL_METHOD_1         1  '1 positional argument'
              300  POP_TOP          

 L. 650   302_304  SETUP_LOOP          606  'to 606'
              306  LOAD_FAST                'kwargs'
              308  LOAD_METHOD              items
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  GET_ITER         
            314_0  COME_FROM           580  '580'
            314_1  COME_FROM           330  '330'
          314_316  FOR_ITER            604  'to 604'
              318  UNPACK_SEQUENCE_2     2 
              320  STORE_FAST               'k'
              322  STORE_FAST               'v'

 L. 651       324  LOAD_FAST                'k'
              326  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              328  COMPARE_OP               in
          330_332  POP_JUMP_IF_FALSE   314  'to 314'

 L. 652       334  LOAD_GLOBAL              SeriesOptions
              336  LOAD_METHOD              __validate_options__
              338  LOAD_FAST                'k'
              340  LOAD_FAST                'v'
              342  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              344  LOAD_FAST                'k'
              346  BINARY_SUBSCR    
              348  CALL_METHOD_3         3  '3 positional arguments'
          350_352  POP_JUMP_IF_FALSE   578  'to 578'

 L. 653       354  LOAD_GLOBAL              isinstance
              356  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              358  LOAD_FAST                'k'
              360  BINARY_SUBSCR    
              362  LOAD_GLOBAL              tuple
              364  CALL_FUNCTION_2       2  '2 positional arguments'
          366_368  POP_JUMP_IF_FALSE   560  'to 560'

 L. 654       370  LOAD_GLOBAL              isinstance
              372  LOAD_FAST                'v'
              374  LOAD_GLOBAL              dict
              376  CALL_FUNCTION_2       2  '2 positional arguments'
          378_380  POP_JUMP_IF_FALSE   414  'to 414'

 L. 655       382  LOAD_FAST                'self'
              384  LOAD_ATTR                __dict__
              386  LOAD_METHOD              update
              388  LOAD_FAST                'k'
              390  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              392  LOAD_FAST                'k'
              394  BINARY_SUBSCR    
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  BUILD_TUPLE_0         0 
              402  LOAD_FAST                'v'
              404  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              406  BUILD_MAP_1           1 
              408  CALL_METHOD_1         1  '1 positional argument'
              410  POP_TOP          
              412  JUMP_FORWARD        558  'to 558'
            414_0  COME_FROM           378  '378'

 L. 656       414  LOAD_GLOBAL              isinstance
              416  LOAD_FAST                'v'
              418  LOAD_GLOBAL              CommonObject
              420  CALL_FUNCTION_2       2  '2 positional arguments'
          422_424  POP_JUMP_IF_TRUE    512  'to 512'
              426  LOAD_GLOBAL              isinstance
              428  LOAD_FAST                'v'
              430  LOAD_GLOBAL              ArrayObject
              432  CALL_FUNCTION_2       2  '2 positional arguments'
          434_436  POP_JUMP_IF_TRUE    512  'to 512'

 L. 657       438  LOAD_GLOBAL              isinstance
              440  LOAD_FAST                'v'
              442  LOAD_GLOBAL              CSSObject
              444  CALL_FUNCTION_2       2  '2 positional arguments'
          446_448  POP_JUMP_IF_TRUE    512  'to 512'
              450  LOAD_GLOBAL              isinstance
              452  LOAD_FAST                'v'
              454  LOAD_GLOBAL              SVGObject
              456  CALL_FUNCTION_2       2  '2 positional arguments'
          458_460  POP_JUMP_IF_TRUE    512  'to 512'
              462  LOAD_GLOBAL              isinstance
              464  LOAD_FAST                'v'
              466  LOAD_GLOBAL              ColorObject
              468  CALL_FUNCTION_2       2  '2 positional arguments'
          470_472  POP_JUMP_IF_TRUE    512  'to 512'

 L. 658       474  LOAD_GLOBAL              isinstance
              476  LOAD_FAST                'v'
              478  LOAD_GLOBAL              JSfunction
              480  CALL_FUNCTION_2       2  '2 positional arguments'
          482_484  POP_JUMP_IF_TRUE    512  'to 512'
              486  LOAD_GLOBAL              isinstance
              488  LOAD_FAST                'v'
              490  LOAD_GLOBAL              Formatter
              492  CALL_FUNCTION_2       2  '2 positional arguments'
          494_496  POP_JUMP_IF_TRUE    512  'to 512'
              498  LOAD_GLOBAL              isinstance
              500  LOAD_FAST                'v'
              502  LOAD_GLOBAL              datetime
              504  LOAD_ATTR                datetime
              506  CALL_FUNCTION_2       2  '2 positional arguments'
          508_510  POP_JUMP_IF_FALSE   530  'to 530'
            512_0  COME_FROM           494  '494'
            512_1  COME_FROM           482  '482'
            512_2  COME_FROM           470  '470'
            512_3  COME_FROM           458  '458'
            512_4  COME_FROM           446  '446'
            512_5  COME_FROM           434  '434'
            512_6  COME_FROM           422  '422'

 L. 659       512  LOAD_FAST                'self'
              514  LOAD_ATTR                __dict__
              516  LOAD_METHOD              update
              518  LOAD_FAST                'k'
              520  LOAD_FAST                'v'
              522  BUILD_MAP_1           1 
              524  CALL_METHOD_1         1  '1 positional argument'
              526  POP_TOP          
              528  JUMP_FORWARD        558  'to 558'
            530_0  COME_FROM           508  '508'

 L. 661       530  LOAD_FAST                'self'
              532  LOAD_ATTR                __dict__
              534  LOAD_METHOD              update
              536  LOAD_FAST                'k'
              538  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              540  LOAD_FAST                'k'
              542  BINARY_SUBSCR    
              544  LOAD_CONST               0
              546  BINARY_SUBSCR    
              548  LOAD_FAST                'v'
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  BUILD_MAP_1           1 
              554  CALL_METHOD_1         1  '1 positional argument'
              556  POP_TOP          
            558_0  COME_FROM           528  '528'
            558_1  COME_FROM           412  '412'
              558  JUMP_FORWARD        576  'to 576'
            560_0  COME_FROM           366  '366'

 L. 663       560  LOAD_FAST                'self'
              562  LOAD_ATTR                __dict__
              564  LOAD_METHOD              update
              566  LOAD_FAST                'k'
              568  LOAD_FAST                'v'
              570  BUILD_MAP_1           1 
              572  CALL_METHOD_1         1  '1 positional argument'
              574  POP_TOP          
            576_0  COME_FROM           558  '558'
              576  JUMP_BACK           314  'to 314'
            578_0  COME_FROM           350  '350'

 L. 665       578  LOAD_FAST                'supress_errors'
          580_582  POP_JUMP_IF_TRUE    314  'to 314'

 L. 665       584  LOAD_GLOBAL              OptionTypeError
              586  LOAD_STR                 'Option Type Mismatch: Expected: %s'
              588  LOAD_GLOBAL              DATA_SERIES_ALLOWED_OPTIONS
              590  LOAD_FAST                'k'
              592  BINARY_SUBSCR    
              594  BINARY_MODULO    
              596  CALL_FUNCTION_1       1  '1 positional argument'
              598  RAISE_VARARGS_1       1  'exception instance'
          600_602  JUMP_BACK           314  'to 314'
              604  POP_BLOCK        
            606_0  COME_FROM_LOOP      302  '302'

Parse error at or near `JUMP_FORWARD' instruction at offset 232

    def __options__(self):
        return self.__dict__

    def __jsonable__(self):
        return self.__dict__