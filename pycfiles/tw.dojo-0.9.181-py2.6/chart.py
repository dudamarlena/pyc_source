# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/chart.py
# Compiled at: 2013-01-02 11:28:41
from tw.dojo.core import DojoBase, JSONHash
from tw.api import Resource, Link, JSLink, JSSource, CSSLink, CSSSource, Widget, js_function, locations
from tw.api import RequestLocalDescriptor
from tw.core.resources import JSDynamicFunctionCalls
animationTypes = {'highlight': 'dojox.charting.action2d.Highlight', 'magnify': 'dojox.charting.action2d.Magnify', 
   'moveslice': 'dojox.charting.action2d.MoveSlice', 
   'shake': 'dojox.charting.action2d.Shake', 
   'tooltip': 'dojox.charting.action2d.Tooltip'}
easingTypes = {'linear': 'dojo.fx.easing.linear', 'quadin': 'dojo.fx.easing.quadIn', 
   'quadout': 'dojo.fx.easing.quadOut', 
   'quadinout': 'dojo.fx.easing.quadInOut', 
   'cubicin': 'dojo.fx.easing.cubicIn', 
   'cubicinout': 'dojo.fx.easing.cubicInOut', 
   'cubicout': 'dojo.fx.easing.cubicOut', 
   'quartin': 'dojo.fx.easing.quartIn', 
   'quartout': 'dojo.fx.easing.quartOut', 
   'quartinout': 'dojo.fx.easing.quartInOut', 
   'quintin': 'dojo.fx.easing.quintIn', 
   'quintout': 'dojo.fx.easing.quintOut', 
   'quintinout': 'dojo.fx.easing.quintInOut', 
   'sinein': 'dojo.fx.easing.sineIn', 
   'sineout': 'dojo.fx.easing.sineOut', 
   'sineinout': 'dojo.fx.easing.sineInOut', 
   'expoin': 'dojo.fx.easing.expoIn', 
   'expoout': 'dojo.fx.easing.expoOut', 
   'expoinout': 'dojo.fx.easing.expoInOut', 
   'circin': 'dojo.fx.easing.circIn', 
   'circout': 'dojo.fx.easing.circOut', 
   'circinout': 'dojo.fx.easing.circInOut', 
   'backin': 'dojo.fx.easing.backIn', 
   'backout': 'dojo.fx.easing.backOut', 
   'backinout': 'dojo.fx.easing.backInOut', 
   'elasticin': 'dojo.fx.easing.elasticIn', 
   'elasticout': 'dojo.fx.easing.elasticOut', 
   'elasticinout': 'dojo.fx.easing.elasticInOut', 
   'bouncein': 'dojo.fx.easing.bounceIn', 
   'bounceout': 'dojo.fx.easing.bounceOut', 
   'bounceinout': 'dojo.fx.easing.bounceInOut'}

class ChartConfigurationError(Exception):
    pass


buildChart = JSSource(src='\n    function buildChart(chart_node,chart_params){\n      var chart = new dojox.charting.Chart2D(chart_node);\n      chart.id="chart_"+chart_node;\n      if (chart_params.axis) for (var i in chart_params.axis) chart.addAxis(chart_params.axis[i].name,chart_params.axis[i].attributes);\n      if (chart_params.plot) for (var i in chart_params.plot) chart.addPlot(chart_params.plot[i].name,chart_params.plot[i].attributes);\n      if (chart_params.series) for (var i in chart_params.series) chart.addSeries(chart_params.series[i].name,chart_params.series[i].series,chart_params.series[i].attributes);\n      \n      if (chart_params.animations) {\n      dojo.require("dojo.fx");\n      dojo.require("dojo.fx.easing");\n      for (var i in chart_params.animations){\n        dojo.require(chart_params.animations[i].type);\n        if (chart_params.animations[i].attributes[\'easing\']) chart_params.animations[i].attributes[\'easing\']=eval(chart_params.animations[i].attributes[\'easing\']);\n        var animation_builder = eval(chart_params.animations[i].type);\n        var animation = new animation_builder(chart,chart_params.animations[i].plot,chart_params.animations[i].attributes);\n      }}\n      chart.render();\n      if (chart_params.legend) {\n        dojo.require("dojox.charting.widget.Legend");\n        chart_params.legend.attributes[\'chart\']=chart;\n        var legend = new dojox.charting.widget.Legend(chart_params.legend.attributes, "legend_"+chart_node);\n        };\n      };\n    ')

class ChartAxis(JSONHash):
    properties = [
     'name']
    attributes_list = [
     'fixLower', 'fixUpper', 'natural', 'min', 'max', 'includeZero', 'majorTicks', 'majorTickStep', 'majorTick', 'labels', 'minorTick',
     'minorTickStep', 'minorLabels', 'microTicks', 'microTickStep', 'microTick', 'microLabels', 'vertical']


class ChartTick(JSONHash):
    attributes_list = [
     'stroke', 'length']


class ChartLabel(JSONHash):
    attributes_list = [
     'value', 'text']


class ChartPlot(JSONHash):
    properties = [
     'name']
    attributes_list = ['type', 'shadows', 'font', 'fontColor', 'labelOffset', 'radius', 'markers', 'tension', 'lines']

    def __init__(self, **kwargs):
        super(ChartPlot, self).__init__(**kwargs)
        if not self.get('name'):
            self['name'] = 'default'


class ChartSeries(JSONHash):
    properties = [
     'name', 'series', 'tuple']
    attributes_list = ['stroke', 'fill']

    def __init__(self, **kwargs):
        super(ChartSeries, self).__init__(**kwargs)
        if self.get('tuple') and self.get('series'):
            new_series = []
            for value in self['series']:
                new_value = {'x': value[0], 'y': value[1]}
                if len(value) > 2:
                    new_value['tooltip'] = value[2]
                new_series.append(new_value)

            self['series'] = new_series


class ChartLegend(JSONHash):
    attributes_list = [
     'horizontal']

    def __init__(self, **kwargs):
        super(ChartLegend, self).__init__(**kwargs)
        if not self.get('horizontal'):
            self['horizontal'] = False


class ChartAnimation(JSONHash):
    properties = [
     'type', 'plot']
    attributes_list = ['highlight', 'duration', 'scale', 'easing']

    def __init__(self, **kwargs):
        super(ChartAnimation, self).__init__(**kwargs)
        if not self.get('plot'):
            self['plot'] = 'default'
        self['type'] = animationTypes.get(self['type'].lower(), None)
        if not self['type']:
            raise ChartConfigurationError, 'Wrong ChartAnimation type attribute'
        if self['attributes'].get('easing'):
            self['attributes']['easing'] = easingTypes.get(self['attributes']['easing'].lower(), None)
            if not self['attributes']['easing']:
                raise ChartConfigurationError, 'Wrong ChartAnimation easing attribute'
        return


class ChartParams(JSONHash):

    def addAxis(self, *axis, **kwargs):
        if axis and isinstance(axis[0], ChartAxis):
            axis = axis[0]
        else:
            axis = ChartAxis(**kwargs)
        if self.get('axis'):
            self['axis'].append(axis)
        else:
            self['axis'] = [
             axis]

    def addPlot(self, *plot, **kwargs):
        if plot and isinstance(plot[0], ChartPlot):
            plot = plot[0]
        else:
            plot = ChartPlot(**kwargs)
        if self.get('plot'):
            self['plot'].append(plot)
        else:
            self['plot'] = [
             plot]

    def addSeries(self, *series, **kwargs):
        if series and isinstance(series[0], ChartSeries):
            series = series[0]
        else:
            series = ChartSeries(**kwargs)
        if self.get('series'):
            self['series'].append(series)
        else:
            self['series'] = [
             series]

    def addAnimation(self, *animation, **kwargs):
        if animation and isinstance(animation[0], ChartAnimation):
            animation = animation[0]
        else:
            animation = ChartAnimation(**kwargs)
        if self.get('animations'):
            self['animations'].append(animation)
        else:
            self['animations'] = [
             animation]

    def addLegend(self, *legend, **kwargs):
        if legend and isinstance(legend[0], ChartLegend):
            legend = legend[0]
        else:
            legend = ChartLegend(**kwargs)
        self['legend'] = legend


class DojoChart2D(DojoBase):
    javascript = [
     buildChart]
    require = ['dojox.charting.Chart2D']
    style = 'width: 400px; height: 200px;'
    attrs = {}
    legend_attrs = {}
    params = ['id', 'attrs', 'style', 'legend_attrs', 'chart_params']
    template = '<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip="">\n    <div id=\'${id}\' py:attrs="dict(attrs)" style="${style}"> </div>\n    <div id=\'legend_${id}\' py:attrs="dict(legend_attrs)"/>\n    <script type=\'text/javascript\'>\n        dojo.addOnLoad(function(){buildChart(\'${id}\',${chart_params});});\n    </script>\n    </span>'

    def __init__(self, **kw):
        self.cparams = kw.get('chart_params', ChartParams())
        super(DojoChart2D, self).__init__(self, **kw)

    def update_params(self, d):
        super(DojoChart2D, self).update_params(d)
        d['chart_params'] = self.cparams.json()

    def addAxis(self, *args, **kwargs):
        self.cparams.addAxis(*args, **kwargs)

    def addPlot(self, *args, **kwargs):
        self.cparams.addPlot(*args, **kwargs)

    def addSeries(self, *args, **kwargs):
        self.cparams.addSeries(*args, **kwargs)

    def addAnimation(self, *args, **kwargs):
        self.cparams.addAnimation(*args, **kwargs)

    def addLegend(self, *args, **kwargs):
        self.cparams.addLegend(*args, **kwargs)