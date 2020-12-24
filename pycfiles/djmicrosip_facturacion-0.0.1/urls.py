# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_facturacion\djmicrosip_facturacion\urls.py
# Compiled at: 2017-09-21 14:27:03
from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^facturar/(?P<id>\\d+)/$', views.facturar), (
 '^factura_ticket/$', views.FacturaTicket), (
 '^mostrar_factura/$', views.mostrar_factura))