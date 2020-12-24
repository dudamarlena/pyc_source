# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/urls.py
# Compiled at: 2011-05-24 10:08:33
from django.conf.urls.defaults import *
from analytics.geckoboard_views import *
from analytics.csv_views import *
urlpatterns = patterns('', (
 '^geckoboard/numbers', geckoboard_number_widget), (
 '^geckoboard/rag', geckoboard_rag_widget), (
 '^geckoboard/pie', geckoboard_pie_chart), (
 '^geckoboard/line', geckoboard_line_chart), (
 '^geckoboard/geckometer', geckoboard_geckometer), (
 '^geckoboard/funnel', geckoboard_funnel), (
 '^csv/(?P<uid>[a-zA-Z0-9\\_]+)', csv_dump))