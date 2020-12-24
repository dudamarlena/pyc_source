# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_reports/highcharts.py
# Compiled at: 2017-09-04 13:31:09
from abc import ABCMeta, abstractmethod
from django_reports.reports import ReportQuery
import json

class PieChartReportQuery(ReportQuery):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_series_data(self, **kwargs):
        pass

    @abstractmethod
    def get_series_name(self, **kwargs):
        pass

    @abstractmethod
    def get_title(self, **kwargs):
        pass

    def eval(self, **kwargs):
        return {'chart': {'plotBackgroundColor': None, 
                     'plotBorderWidth': None, 
                     'plotShadow': False, 
                     'type': 'pie'}, 
           'title': {'text': self.get_title(**kwargs)}, 
           'tooltip': {'pointFormat': '{series.name}: <b>{point.y:.1f}%</b>'}, 
           'plotOptions': {'pie': {'allowPointSelect': True, 
                                   'cursor': 'pointer', 
                                   'dataLabels': {'enabled': True, 
                                                  'format': '<b>{point.name}</b>: {point.y:.1f} %', 
                                                  'style': {'color': 'black'}}}}, 
           'series': [
                    {'name': self.get_series_name(**kwargs), 
                       'colorByPoint': True, 
                       'data': self.get_series_data(**kwargs)}]}


class BarChartReportQuery(ReportQuery):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_series_names(self, **kwargs):
        return ['series 1', 'series 2']

    @abstractmethod
    def get_series_data(self, series, **kwargs):
        return [1.0, 2.1, 1.5, 0.4]

    @abstractmethod
    def get_x_labels(self, **kwargs):
        return ['May', 'June', 'July', 'August']

    @abstractmethod
    def get_title(self, **kwargs):
        return 'Bar Chart'

    @abstractmethod
    def get_y_title(self, **kwargs):
        return 'Average'

    def eval(self, **kwargs):
        return {'chart': {'type': 'column'}, 
           'title': {'text': self.get_title(**kwargs)}, 
           'xAxis': {'categories': self.get_x_labels(**kwargs)}, 
           'yAxis': {'min': 0, 
                     'title': {'text': self.get_y_title(**kwargs)}, 
                     'stackLabels': {'enabled': True, 
                                     'style': {'fontWeight': 'bold', 
                                               'color2': 'gray'}}}, 
           'legend': {'align': 'right', 
                      'x': -30, 
                      'verticalAlign': 'top', 
                      'y': 25, 
                      'floating': True, 
                      'backgroundColor': 'white', 
                      'borderColor': '#CCC', 
                      'borderWidth': 1, 
                      'shadow': False}, 
           'tooltip': {'headerFormat': '<b>{point.x}</b><br/>', 
                       'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'}, 
           'plotOptions': {'column': {'stacking': 'normal', 
                                      'dataLabels': {'enabled': True, 
                                                     'color': 'white'}}}, 
           'series': [ {'name': s, 'colorByPoint': True, 'data': self.get_series_data(s, **kwargs)} for s in self.get_series_names(**kwargs)
                   ]}