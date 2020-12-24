# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chart/urls.py
# Compiled at: 2010-08-04 03:51:07
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('chart.views', url('^(?P<slug>[\\w-]+)/$', 'object_detail', name='chart_object_detail'))