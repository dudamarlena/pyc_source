# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\urls.py
# Compiled at: 2019-09-17 20:13:06
from django.conf.urls import patterns, url, include
from . import views
from inventarios_fisicos import urls as inventario_urls
from .almacenes import urls as almacenes_urls
from .herramientas import urls as herramientas_urls
from core import urls as core_urls
urlpatterns = patterns('', (
 '^$', views.index), (
 '^ayuda/$', views.ayuda), (
 '^close_inventario_byalmacen_view/$', views.close_inventario_byalmacen_view), (
 '^getlogs_ini/$', views.getlogs_ini), (
 '^setlogs_ini/$', views.setlogs_ini), (
 '^add_articulossinexistencia/$', views.add_articulossinexistencia), (
 '^add_articulossinexistencia_bylinea/$', views.add_articulossinexistencia_bylinea), url('', include(core_urls, namespace='core')), url('almacenes/', include(almacenes_urls, namespace='almacenes')), url('herramientas/', include(herramientas_urls, namespace='herramientas')), url('inventarios_fisicos/', include(inventario_urls, namespace='inventarios_fisicos')))