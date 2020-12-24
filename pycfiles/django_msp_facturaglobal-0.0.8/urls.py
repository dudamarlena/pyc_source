# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django_msp_facturaglobal\django_msp_facturaglobal\urls.py
# Compiled at: 2014-12-10 15:06:48
from django.conf.urls import patterns, url
from .views import index, generar_factura_global, VentasPorFacturarList, generar_venta_factura
urlpatterns = patterns('', (
 '^$', index), (
 '^generar_factura_global/$', generar_factura_global), (
 '^generar_venta_factura/$', generar_venta_factura), (
 '^ventas_por_facturar/$', VentasPorFacturarList.as_view()), (
 '^ventas_por_facturar/(?P<start_date>\\d+)/(?P<end_date>\\d+)/$', VentasPorFacturarList.as_view()))