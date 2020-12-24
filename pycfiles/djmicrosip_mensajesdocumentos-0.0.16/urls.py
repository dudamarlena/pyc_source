# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_mensajesdocumentos\djmicrosip_mensajesdocumentos\urls.py
# Compiled at: 2015-06-29 16:44:29
from django.conf.urls import patterns, url
from .views import index, preparar_aplicacion, preferencias_manageview, send_messages
urlpatterns = patterns('', (
 '^$', index), (
 'preferencias/actualizar_tablas/$', preparar_aplicacion), (
 'preferencias/preferencias/$', preferencias_manageview), (
 'send_messages/$', send_messages))