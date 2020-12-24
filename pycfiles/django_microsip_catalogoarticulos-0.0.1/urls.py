# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_microsip_catalogoarticulos\django_microsip_catalogoarticulos\urls.py
# Compiled at: 2014-10-15 12:19:38
from django.conf.urls import patterns, url
from .views import index, ArticulosView, ArticuloManageView, TagsManageView, TagsView, AgregarTagArticulo, EliminarTagArticulo, UpdateDatabaseTable
urlpatterns = patterns('', (
 '^$', ArticulosView), (
 '^articulos/$', ArticulosView), (
 '^articulo/$', ArticuloManageView), (
 '^articulo/(?P<id>\\d+)/', ArticuloManageView), (
 '^tag/$', TagsManageView), (
 '^tag/(?P<id>\\d+)/', TagsManageView), (
 '^tags/$', TagsView), (
 '^agregar_tag_articulo/$', AgregarTagArticulo), (
 '^eliminar_tag_articulo/$', EliminarTagArticulo), (
 '^inicializar/$', UpdateDatabaseTable))