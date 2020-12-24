# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webplotlib/test_chart_builders.py
# Compiled at: 2011-05-24 20:00:42
"""
Tests for the webplotlib package.
"""
import pytest
from webplotlib.chart_builders import create_chart_as_png_str

class TestChartBuildersTimeseries:

    def setup_method(self, method):
        self.ts_data = [
         1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    def test_timeseries(self):
        vis_data = {'data': [
                  self.ts_data], 
           'names': [
                   'Fibonacci Numbers'], 
           'colors': [
                    '#7C8BD9'], 
           'linestyles': [
                        '-']}
        vis_labels = {'title': 'First Ten Fibonacci Numbers', 
           'x': 'Sequence Number', 
           'y': 'Fibonacci Number'}
        chart_png_str = create_chart_as_png_str('timeseries', vis_data, labels_dct=vis_labels, template='clean')
        assert hash(chart_png_str) == -7569801611015431504


class TestChartBuildersBarcharts:

    def setup_method(self, method):
        self.bar_data = [
         1, 3, 5, 2, 6, 8.1, -2.3, 4.3, 5.9, 9]

    def test_timeseries(self):
        vis_data = {'data': [
                  self.bar_data], 
           'names': [
                   'Foo Data'], 
           'colors': [
                    '#7C8BD9']}
        vis_labels = {'title': 'Some Kind of Data', 
           'x': 'Data', 
           'y': 'Value'}
        chart_png_str = create_chart_as_png_str('barchart', vis_data, labels_dct=vis_labels, template='clean')
        assert hash(chart_png_str) == 6805953041015498766


class TestChartBuildersBadInputs:

    def setup_method(self, method):
        self.bar_data = [
         1, 3, 5, 2, 6, 8.1, -2.3, 4.3, 5.9, 9]

    def test_bad_chart_type(self):
        vis_data = {'data': [
                  self.bar_data], 
           'names': [
                   'Foo barchart data']}
        vis_labels = {'title': 'Some Kind of Data', 
           'x': 'Data', 
           'y': 'Value'}
        with pytest.raises(AssertionError):
            chart_png_str = create_chart_as_png_str('foo', vis_data, labels_dct=vis_labels, template='clean')

    def test_bad_chart_data(self):
        vis_data = [1, 2, 3, 4, 5]
        vis_labels = {'title': 'Some Kind of Data', 
           'x': 'Data', 
           'y': 'Value'}
        with pytest.raises(AssertionError):
            chart_png_str = create_chart_as_png_str('timeseries', vis_data, labels_dct=vis_labels, template='clean')

    def test_bad_chart_data_two(self):
        vis_data = {'data': [[], []], 'names': [
                   'Foo data']}
        vis_labels = {'title': '', 
           'x': '', 
           'y': ''}
        with pytest.raises(AssertionError):
            chart_png_str = create_chart_as_png_str('barchart', vis_data, labels_dct=vis_labels, template='clean')

    def test_bad_chart_labels(self):
        vis_data = {'data': [
                  self.bar_data], 
           'names': [
                   'Foo barchart data']}
        vis_labels = {'foo': 'bar'}
        with pytest.raises(AssertionError):
            chart_png_str = create_chart_as_png_str('barchart', vis_data, labels_dct=vis_labels, template='clean')