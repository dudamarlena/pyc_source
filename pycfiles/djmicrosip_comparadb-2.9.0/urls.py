# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_comparadb\djmicrosip_comparadb\urls.py
# Compiled at: 2016-12-16 11:53:55
from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^compara_articulos/$', views.articulos_view), (
 '^nuevos_articulos/$', views.articulos2_view), (
 '^renombrar_articulos/$', views.renombrar_articulos_view), (
 '^localizaciones/$', views.localizaciones_view), (
 '^costosultimo/$', views.costosultimo_view), (
 '^costosprom/$', views.costosprom_view), (
 '^precios_linea/$', views.precios_linea_view), (
 '^sync/$', views.sync_view), (
 '^exporta_excel/$', views.exporta_excel_view))