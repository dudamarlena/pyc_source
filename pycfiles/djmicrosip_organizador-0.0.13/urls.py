# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_organizador\djmicrosip_organizador\urls.py
# Compiled at: 2015-02-16 13:31:38
from django.conf.urls import patterns, url
from .views import *
urlpatterns = patterns('', (
 '^$', ArticuloListView.as_view()), (
 '^get_structure/$', get_estructura_carpetas), (
 '^get_articles_in_folder/$', get_articles_in_folder), (
 '^get_articles_in_folder_all/$', get_articles_in_folder_all), (
 '^set_article_in_folder/$', set_article_in_folder), (
 '^articulos/$', ArticuloListView.as_view()), (
 '^articulo/$', ArticuloManageView), (
 '^articulo/(?P<id>\\d+)/', ArticuloManageView), (
 '^herramientas/sync/$', updateDatabaseView), (
 '^agregar_tag_articulo/$', agregar_tag_articulo), (
 '^consulta_articulos/$', articles_search), (
 '^move_articles/$', move_articles), (
 '^get_folder_id/$', get_folder_id), (
 '^create_folder/$', create_folder), (
 '^remove_folder/$', remove_folder), (
 '^rename_folder/$', rename_folder), (
 '^move_folder/$', move_folder), (
 '^tags/$', TagListView.as_view()), (
 '^tag/$', TagsManageView), (
 '^tag/(?P<id>\\d+)/', TagsManageView), (
 '^eliminartag/(?P<id>\\d+)/', EliminarTag), (
 '^inicializar/$', UpdateDatabaseTable))