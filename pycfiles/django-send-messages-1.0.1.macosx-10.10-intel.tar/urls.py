# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/esperyong/develop/pyprojects/hwbuluo_src/hwbuluo-site/venv/lib/python2.7/site-packages/testproj/urls.py
# Compiled at: 2015-05-11 01:18:10
from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('', url('^admin/', include(admin.site.urls)), url('^', include('sms.urls')))