# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_cambiaprecios\djmicrosip_cambiaprecios\urls.py
# Compiled at: 2017-05-03 15:46:28
from django.conf.urls import patterns, url, include
from .views import index, articulo_manageview, ArticuloListView
from .modulos.herramientas import urls as herramientas_urls
urlpatterns = patterns('', (
 '^$', index), (
 '^articulo/$', articulo_manageview), (
 '^articulo/(?P<id>\\d+)/', articulo_manageview), (
 '^articulo_mobile/(?P<id>\\d+)/', articulo_manageview, {'template_name': 'djmicrosip_cambiaprecios/articulo_mobile.html'}), (
 '^articulos/$', ArticuloListView.as_view()), url('', include(herramientas_urls, namespace='herramientas')))