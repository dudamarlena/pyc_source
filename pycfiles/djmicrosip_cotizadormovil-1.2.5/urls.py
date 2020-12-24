# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizadormovil\djmicrosip_cotizadormovil\urls.py
# Compiled at: 2015-05-19 12:21:31
from django.conf.urls import patterns, url
from .views import index, cotizacionView, PreferenciasManageView, UpdateDatabaseTable, GetPrecioArticulo, GetArticulobyClave, SearchArticulos, CreaDocumento
urlpatterns = patterns('', (
 '^$', index), (
 '^cotizacion/$', cotizacionView), (
 '^preferencias/$', PreferenciasManageView), (
 '^preferencias/actualizar_bd/$', UpdateDatabaseTable), (
 '^get_precio/$', GetPrecioArticulo), (
 '^articulo_by_clave/$', GetArticulobyClave), (
 '^articulos_search/$', SearchArticulos), (
 '^crea_documento/$', CreaDocumento))