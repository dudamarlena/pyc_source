# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/danielwatkins/dev/django-rest-test-data/rest_test_data/urls.py
# Compiled at: 2013-11-25 05:05:24
# Size of source mod 2**32: 560 bytes
from django.conf.urls import patterns, url
from rest_test_data.views import TestDataModelRestView, TestDataDetailRestView, TestDataSearchRestView
urlpatterns = patterns('', url('^(?P<app>[^/]+)/(?P<model>[^/]+)/$', TestDataModelRestView.as_view(), name='objects'), url('^(?P<app>[^/]+)/(?P<model>[^/]+)/search/$', TestDataSearchRestView.as_view(), name='search'), url('^(?P<app>[^/]+)/(?P<model>[^/]+)/(?P<pk>\\d+)/$', TestDataDetailRestView.as_view(), name='object'))