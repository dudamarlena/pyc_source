# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reorden\djmicrosip_reorden\urls.py
# Compiled at: 2016-02-03 17:34:37
from django.conf.urls import patterns
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^generar/$', views.genera_view), (
 '^generar_entradas/$', views.generaentrada_view), (
 '^generar_pedido/$', views.generapedido_view), (
 '^entradas_automaticas/$', views.entradas_automaticas_view), (
 '^salidas_automaticas/$', views.salidas_automaticas_view), (
 '^generar_auto/$', views.genera_auto_view), (
 '^preferencias/$', views.preferencias_view), (
 '^actualizar/$', views.UpdateDatabaseTable), (
 '^crea_documento/$', views.crea_documento_view))