# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_sms\django_msp_sms\urls.py
# Compiled at: 2015-10-19 12:15:02
from django.conf.urls import patterns, url, include
from . import views
from .modulos.preferencias import urls as preferencias_urls
from .modulos.personalizados import urls as personalizados_urls
from .modulos.saldos_clientes import urls as saldos_clientes_urls
from .modulos.clientes import urls as clientes_urls
urlpatterns = patterns('', (
 '^$', views.index), (
 '^enviar_sms/$', views.enviar_smsView), (
 '^enviar_mensaje/$', views.enviar_mensaje), (
 '^get_creditos/$', views.get_creditos), (
 '^get_mensajes_personalizados/$', views.get_mensajes_personalizados), (
 '^personalizados/por_telefono/$', views.personalizadosView), url('', include(preferencias_urls, namespace='preferencias')), url('', include(personalizados_urls, namespace='personalizados')), url('', include(saldos_clientes_urls, namespace='saldos_clientes')), url('', include(clientes_urls, namespace='clientes')))