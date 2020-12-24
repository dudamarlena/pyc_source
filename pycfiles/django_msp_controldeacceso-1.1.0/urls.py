# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_controldeacceso\django_msp_controldeacceso\urls.py
# Compiled at: 2016-02-15 12:30:53
from django.conf.urls import patterns, url
from .views import index, cliente_search, UpdateDatabaseTable, ClienteListView, ClienteManageView, PreferenciasManageView, play_sound, log_view, ImagenManageView, ImagenListView, eliminarimagen
urlpatterns = patterns('', (
 '^$', index), (
 '^search/$', cliente_search), (
 '^initialize/$', UpdateDatabaseTable), (
 '^clientes/$', ClienteListView.as_view()), (
 '^cliente/(?P<id>\\d+)/', ClienteManageView), (
 '^preferencias/$', PreferenciasManageView), (
 '^play_sound/$', play_sound), (
 '^bitacora/$', log_view), (
 '^imagenes/$', ImagenListView.as_view()), (
 '^imagen/$', ImagenManageView), (
 '^imagen/(?P<id>\\d+)/', ImagenManageView), (
 '^eliminarimagen/(?P<id>\\d+)/', eliminarimagen))