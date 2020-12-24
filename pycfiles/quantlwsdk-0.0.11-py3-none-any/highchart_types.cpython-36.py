# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
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
            else:
                return False

    def __options__(self):
        return self.__dict__

    def __jsonable__(self):
        return self.__dict__

    def update(self, series_type, **kwargs):
        allowed_args = PLOT_OPTION_ALLOWED_ARGS[series_type]
        allowed_args.update(PLOT_OPTION_ALLOWED_ARGS['common'])
        for k, v in kwargs.items():
            if k in allowed_args:
                if SeriesOptions.__validate_options__(k, v, allowed_args[k]):
                    if isinstance(allowed_args[k], tuple):
                        if isinstance(allowed_args[k][0](), CommonObject):
                            if self.__getattr__(k):
                                if isinstance(v, dict):
                                    self.__options__()[k].update(v)
                                else:
                                    self.__options__()[k].__options__().update(v)
                            else:
                                self.__options__().update({k: (allowed_args[k][0])(**v)})
                    if isinstance(allowed_args[k], tuple) and isinstance(allowed_args[k][0](), ArrayObject):
                        if isinstance(v, dict):
                            self.__dict__[k].append((allowed_args[k][0])(**v))
                        else:
                            if isinstance(v, list):
                                for item in v:
                                    self.__dict__[k].append((allowed_args[k][0])(**item))

                            else:
                                OptionTypeError('Not An Accepted Input Type: %s' % type(v))
                    elif isinstance(allowed_args[k], tuple):
                        if isinstance(allowed_args[k][0](), CSSObject) or isinstance(allowed_args[k][0](), SVGObject):
                            if self.__getattr__(k):
                                for key, value in v.items():
                                    self.__dict__[k].__options__().update({key: value})

                            else:
                                self.__dict__.update({k: (allowed_args[k][0])(**v)})
                            v = self.__dict__[k].__options__()
                            if isinstance(v, dict):
                                self.__dict__.update({k: (allowed_args[k][0])(**v)})
                            else:
                                self.__dict__.update({k: allowed_args[k][0](v)})
                    elif isinstance(allowed_args[k], tuple):
                        if isinstance(allowed_args[k][0](), JSfunction) or isinstance(allowed_args[k][0](), Formatter) or isinstance(allowed_args[k][0](), ColorObject):
                            if isinstance(v, dict):
                                self.__dict__.update({k: (allowed_args[k][0])(**v)})
                            else:
                                self.__dict__.update({k: allowed_args[k][0](v)})
                    else:
                        self.__dict__.update({k: v})
                else:
                    print(k, v)
                    if not supress_errors:
                        raise OptionTypeError('Option Type Mismatch: Expected: %s' % allowed_args[k])

    def process_kwargs(self, kwargs, series_type, supress_errors=False):
        allowed_args = PLOT_OPTION_ALLOWED_ARGS[series_type]
        allowed_args.update(PLOT_OPTION_ALLOWED_ARGS['common'])
        for k, v in kwargs.items():
            if k in allowed_args:
                if SeriesOptions.__validate_options__(k, v, allowed_args[k]):
                    if isinstance(allowed_args[k], tuple):
                        if isinstance(v, dict):
                            self.__dict__.update({k: (allowed_args[k][0])(**v)})
                        else:
                            if isinstance(v, list):
                                if len(v) == 1:
                                    self.__dict__.update({k: (allowed_args[k][0])(**v[0])})
                                else:
                                    self.__dict__.update({k: (allowed_args[k][0])(**v[0])})
                                    for item in v[1:]:
                                        self.__dict__[k].update(item)

                            else:
                                if isinstance(v, CommonObject) or isinstance(v, ArrayObject) or isinstance(v, CSSObject) or isinstance(v, SVGObject) or isinstance(v, ColorObject) or isinstance(v, JSfunction) or isinstance(v, Formatter) or isinstance(v, datetime.datetime):
                                    self.__dict__.update({k: v})
                                else:
                                    self.__dict__.update({k: allowed_args[k][0](v)})
                    else:
                        self.__dict__.update({k: v})
                else:
                    print(k, v)
                    if not supress_errors:
                        raise OptionTypeError('Option Type Mismatch: Expected: %s' % allowed_args[k])

    def load_defaults(self, series_type):
        self.process_kwargs(DEFAULT_OPTIONS.get(series_type, {}), series_type)

    def __getattr__(self, item):
        if item not in self.__dict__:
            return
        else:
            return True


class Series(object):
    __doc__ = 'Series class for input data '

    def __init__(self, data, series_type='line', supress_errors=False, **kwargs):
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if k in DATA_SERIES_ALLOWED_OPTIONS and SeriesOptions.__validate_options__(k, v, DATA_SERIES_ALLOWED_OPTIONS[k]):
                            if isinstance(DATA_SERIES_ALLOWED_OPTIONS[k], tuple):
                                if isinstance(v, dict):
                                    item.update({k: (DATA_SERIES_ALLOWED_OPTIONS[k][0])(**v)})
                                else:
                                    if isinstance(v, CommonObject) or isinstance(v, ArrayObject) or isinstance(v, CSSObject) or isinstance(v, SVGObject) or isinstance(v, ColorObject) or isinstance(v, JSfunction) or isinstance(v, Formatter) or isinstance(v, datetime.datetime):
                                        item.update({k: v})
                                    else:
                                        item.update({k: DATA_SERIES_ALLOWED_OPTIONS[k][0](v)})
                            else:
                                item.update({k: v})

        self.__dict__.update({'data':data, 
         'type':series_type})
        for k, v in kwargs.items():
            if k in DATA_SERIES_ALLOWED_OPTIONS:
                if SeriesOptions.__validate_options__(k, v, DATA_SERIES_ALLOWED_OPTIONS[k]):
                    if isinstance(DATA_SERIES_ALLOWED_OPTIONS[k], tuple):
                        if isinstance(v, dict):
                            self.__dict__.update({k: (DATA_SERIES_ALLOWED_OPTIONS[k][0])(**v)})
                        else:
                            if isinstance(v, CommonObject) or isinstance(v, ArrayObject) or isinstance(v, CSSObject) or isinstance(v, SVGObject) or isinstance(v, ColorObject) or isinstance(v, JSfunction) or isinstance(v, Formatter) or isinstance(v, datetime.datetime):
                                self.__dict__.update({k: v})
                            else:
                                self.__dict__.update({k: DATA_SERIES_ALLOWED_OPTIONS[k][0](v)})
                    else:
                        self.__dict__.update({k: v})
                elif not supress_errors:
                    raise OptionTypeError('Option Type Mismatch: Expected: %s' % DATA_SERIES_ALLOWED_OPTIONS[k])

    def __options__(self):
        return self.__dict__

    def __jsonable__(self):
        return self.__dict__