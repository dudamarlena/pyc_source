# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_clasificadores\djmicrosip_clasificadores\urls.py
# Compiled at: 2020-04-15 11:51:04
from django.conf.urls import patterns, url
from .views import *
urlpatterns = patterns('', (
 '^$', index), (
 '^preferencias/$', preferencias), (
 '^get_todos_almacenes/$', get_todos_almacenes), (
 '^compatibilidad_articulo/$', compatibilidad_articulo), (
 '^actualiza_base_datos/$', actualiza_base_datos), (
 '^crear_pedido_temporal/$', crear_pedido_temporal), (
 '^clasificador_asignacion/$', clasificador_asignacion), (
 '^crear_usuarios_clientes/$', crear_usuarios_clientes), (
 '^usuario_cliente/$', usuario_cliente), (
 '^cambiar_contrasena/$', cambiar_contrasena), (
 '^recuperar_contrasena/$', recuperar_contrasena), (
 '^find_user/$', find_user), (
 '^enviar_contrasena/(?P<id>\\d+)/$', enviar_contrasena), (
 '^compatibilidad_articulos/$', compatibilidad_articulos), (
 '^guardar_articulos_compatibles/$', guardar_articulos_compatibles), (
 '^asignar_compatibilidad_articulos/(?P<id>\\d+)/$', asignar_compatibilidad_articulos), (
 '^eliminar_detalle/(?P<id_detalle>\\d+)/(?P<id_pedido>\\d+)/$', eliminar_detalle), (
 '^view_pedido/(?P<id>\\d+)/$', view_pedido))