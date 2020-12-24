# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_utilerias\djmicrosip_utilerias\urls.py
# Compiled at: 2015-03-07 12:47:32
from django.conf.urls import patterns, url
from .views import index, actualiza_margenes_view, get_articulos_ids, actualiza_margenes_ajax, exportar_precios, importar_precios
urlpatterns = patterns('', (
 '^$', index), (
 '^actualiza_margenes/$', actualiza_margenes_view), (
 '^get_articulos_ids/$', get_articulos_ids), (
 '^actualiza_margenes_ajax/$', actualiza_margenes_ajax), (
 '^exportar_precios/$', exportar_precios), (
 '^importar_precios/$', importar_precios))