# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_analytics/urls.py
# Compiled at: 2016-08-25 04:11:26
from django.conf.urls import patterns, include, url
urlpatterns = patterns('', url('^google-analytics/$', 'jmbo_analytics.views.google_analytics.google_analytics', {}, 'google-analytics'))