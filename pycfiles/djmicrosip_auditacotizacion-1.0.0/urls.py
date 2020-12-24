# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_auditacotizacion\djmicrosip_auditacotizacion\urls.py
# Compiled at: 2015-12-08 11:45:26
from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^audita/$', views.audita_view), (
 '^articulo_by_clave/$', views.GetArticulobyClave), (
 '^crea_documento/$', views.CreaDocumento))