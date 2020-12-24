# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_consultaprecio\django_microsip_consultaprecio\urls.py
# Compiled at: 2015-11-13 19:01:52
from django.conf.urls import patterns, url
from .views import index, PrecioArticuloView, PreferenciasManageView, InitialzeConfigurationDatabase, imagen_manageview, eliminarimagen
urlpatterns = patterns('', (
 '^$', index), (
 '^precio/$', PrecioArticuloView), (
 '^inicializar/$', InitialzeConfigurationDatabase), (
 '^preferencias/$', PreferenciasManageView), (
 '^imagen/$', imagen_manageview), (
 '^imagen/(?P<id>\\d+)/', imagen_manageview), (
 '^imagen/delete/(?P<id>\\d+)/', eliminarimagen))