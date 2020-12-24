# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/Projects/DjangoProjects/basitapi/basitapi/tests/urls.py
# Compiled at: 2013-04-25 14:18:17
from django.conf.urls import patterns, url
from basitapi.urlpatterns import format_suffix_patterns
from basitapi.tests.integration_tests import views_tests
urlpatterns = patterns('', url('sample$', views_tests.SampleView.as_view()), url('error$', views_tests.SampleErrorView.as_view()))
urlpatterns = format_suffix_patterns(urlpatterns)