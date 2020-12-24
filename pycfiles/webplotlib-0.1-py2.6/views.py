# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webplotlib/views.py
# Compiled at: 2011-05-24 18:47:12
from django.http import HttpResponse, HttpResponseRedirect
from webplotlib.chart_builders import create_chart_as_png_str

def index(request):
    return HttpResponseRedirect('/admin/')


def show_ts_plot_png(request):
    fake_data_dct = {'data': [
              [
               1, 2, 1, 2, 3, -1, 4, -2, 2.5, 1.3]]}
    img_str = create_chart_as_png_str('timeseries', fake_data_dct, {}, '')
    response = HttpResponse(img_str, mimetype='image/png')
    return response


def show_bar_plot_png(request):
    fake_data_dct = {'data': [
              [
               1, 2, 1, 2, 3, -11, 4, -2, 2.5, 1.3]]}
    img_str = create_chart_as_png_str('barchart', fake_data_dct, {}, '')
    response = HttpResponse(img_str, mimetype='image/png')
    return response