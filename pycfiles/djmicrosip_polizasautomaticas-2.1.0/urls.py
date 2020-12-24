# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizasautomaticas\djmicrosip_polizasautomaticas\urls.py
# Compiled at: 2018-07-04 11:44:54
from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^preferencias/$', views.preferencias_view), (
 '^actualizar_db/$', views.UpdateDatabaseView), (
 '^crear_polizas/$', views.crear_polizas_view), (
 '^crea_anteriores/$', views.crea_anteriores_view), (
 '^reemplaza_cuenta/$', views.reemplaza_view), (
 '^separa_ventas/$', views.SeparaVentas), (
 '^recalculo_saldos/$', views.recalculo_view), (
 '^log/$', views.log_view), (
 '^elimina_log/$', views.elimina_log_view))