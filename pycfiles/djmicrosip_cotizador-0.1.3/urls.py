# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizador\djmicrosip_cotizador\urls.py
# Compiled at: 2015-03-17 17:54:10
from django.conf.urls import patterns, url, include
from .views import index, updateDatabaseView, EstructurasList, EstructurasManageView, EliminarEstructura, EditarEstructura, DetallesManageView, GetNodeStructure, get_folder_children, get_folderfullpath
from .cotizar import urls as cotizar_urls
urlpatterns = patterns('', url('^cotizar/', include(cotizar_urls, namespace='cotizar')), (
 '^$', index), (
 '^herramientas/sync/$', updateDatabaseView), (
 '^estructuras/$', EstructurasList.as_view()), (
 '^estructura/$', EstructurasManageView), (
 '^estructura/(?P<id>\\d+)$', EstructurasManageView), (
 '^eliminarestructura/(?P<id>\\d+)$', EliminarEstructura), (
 '^editarestructura/(?P<est_id>\\d+)$', EditarEstructura), (
 '^get_node_structure/$', GetNodeStructure), (
 '^get_folder_childresn/$', get_folder_children), (
 '^get_folderfullpath/$', get_folderfullpath), (
 '^detalle/(?P<est_id>\\d+)$', DetallesManageView), (
 '^detalle/(?P<est_id>\\d+)/(?P<det_id>\\d+)$', DetallesManageView))