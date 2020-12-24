# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reportes\djmicrosip_reportes\urls.py
# Compiled at: 2016-06-24 18:51:08
from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^existencias_linea/$', views.existencia_linea))