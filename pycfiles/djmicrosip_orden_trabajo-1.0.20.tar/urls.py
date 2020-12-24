# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_orden_trabajo\djmicrosip_orden_trabajo\urls.py
# Compiled at: 2020-01-16 13:17:47
from django.conf.urls import patterns, url
from .views import *
urlpatterns = patterns('', (
 '^$', index), (
 '^info_cliente/$', info_cliente), (
 '^pedido/(?P<id>\\d+)/$', add_pedido), (
 '^inf_articulo/$', inf_articulo), (
 '^vendedor_asignar/$', vendedor_asignar), (
 '^get_detalles/$', get_detalles), (
 '^change_progress/$', change_progress), (
 '^fin_progress/$', fin_progress), (
 '^return_progress/$', return_progress), (
 '^get_tiempos/$', get_tiempos), (
 '^actualiza_base_datos/$', actualiza_base_datos), (
 '^preferencias/$', preferencias), (
 '^nota_pedido/(?P<id_doc>\\d+)/$', nota_pedido), (
 '^firma/(?P<id_crm>\\d+)/$', firma), (
 '^enviar_correo/$', enviar_correo), (
 '^lista_vendedores/$', lista_vendedores), (
 '^configuracion_usuarios_onesignal/(?P<id_vendedor>\\d+)/$', configuracion_usuarios_onesignal), (
 '^search_id/$', search_id), (
 '^send_notifications_preprogramadas/$', send_notifications_preprogramadas))