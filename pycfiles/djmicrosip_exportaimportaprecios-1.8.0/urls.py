# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_exportaimportaprecios\djmicrosip_exportaimportaprecios\urls.py
# Compiled at: 2016-02-05 12:45:42
from django.conf.urls import patterns, url
from .views import index, exportar_precios_view, importar_precios_view
urlpatterns = patterns('', (
 '^$', index), (
 '^exportar_precios/$', exportar_precios_view), (
 '^importar_precios/$', importar_precios_view))