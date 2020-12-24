# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_mail\djmicrosip_mail\urls.py
# Compiled at: 2019-12-02 13:48:11
from django.conf.urls import patterns, url, include
from .views import index, envia_saldos_automaticos
from .modulos.clientes import urls as clientes_urls
from .modulos.personalizados import urls as personalizados_urls
from .modulos.saldos_clientes import urls as saldos_clientes_urls
from .modulos.herramientas import urls as herramientas_urls
urlpatterns = patterns('', (
 '^$', index), (
 'saldos/todos_automatico/$', envia_saldos_automaticos), url('', include(clientes_urls, namespace='clientes')), url('', include(personalizados_urls, namespace='personalizados')), url('', include(saldos_clientes_urls, namespace='saldos_clientes')), url('', include(herramientas_urls, namespace='herramientas')))