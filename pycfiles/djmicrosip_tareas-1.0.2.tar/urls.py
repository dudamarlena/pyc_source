# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_tareas\djmicrosip_tareas\urls.py
# Compiled at: 2020-01-17 20:06:16
from django.conf.urls import patterns, url, include
from .views import index, tareas, tarea, tarea_delete
from .herramientas import urls as herramientas_urls
urlpatterns = patterns('', (
 '^$', index), (
 '^tareas/$', tareas), (
 '^tarea/$', tarea), (
 '^tarea/(?P<id>\\d+)/$', tarea), (
 '^tarea_delete/(?P<id>\\d+)/$', tarea_delete), url('herramientas/', include(herramientas_urls, namespace='herramientas')))