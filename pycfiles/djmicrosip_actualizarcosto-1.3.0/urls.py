# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_actualizarcosto\djmicrosip_actualizarcosto\urls.py
# Compiled at: 2016-02-19 15:09:36
from django.conf.urls import patterns, url
from .views import index, actualizarView, ArticuloManageView, GetArticulobyClave
urlpatterns = patterns('', (
 '^$', index), (
 '^actualizar/$', actualizarView), (
 '^articulo/(?P<id>\\d+)/', ArticuloManageView), (
 '^articulo_by_clave/$', GetArticulobyClave))