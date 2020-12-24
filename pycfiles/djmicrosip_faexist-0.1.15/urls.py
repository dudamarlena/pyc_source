# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_faexist\djmicrosip_faexist\urls.py
# Compiled at: 2015-01-22 15:54:16
from django.conf.urls import patterns, url
from .views import index, exporta_factura, preferencias, GetProveedoresByEmpresa, GuardarPreferencias, GenerarCompras, GetAlmacenesByEmpresa, UpdateDatabaseTable, ArticuloListView, ignorar_articulos
urlpatterns = patterns('', (
 '^$', index), (
 '^exporta_factura/$', exporta_factura), (
 '^preferencias/$', preferencias), (
 '^get_proveedores_byempresa/$', GetProveedoresByEmpresa), (
 '^get_almacenes_byempresa/$', GetAlmacenesByEmpresa), (
 '^guardar_preferencias/$', GuardarPreferencias), (
 '^generar_compras/$', GenerarCompras), (
 '^preferencias/actualizar_tablas/$', UpdateDatabaseTable), (
 '^articulos/$', ArticuloListView.as_view()), (
 '^ignorar_articulos/$', ignorar_articulos))