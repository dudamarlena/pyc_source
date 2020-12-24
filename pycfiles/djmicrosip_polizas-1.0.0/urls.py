# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizas\djmicrosip_polizas\urls.py
# Compiled at: 2016-04-13 11:53:07
from django.conf.urls import patterns, url, include
from .views import index
from .modulos.preferencias import urls as preferencias_urls
from .modulos.polizas import urls as polizas_urls
urlpatterns = patterns('', (
 '^$', index), url('', include(polizas_urls, namespace='polizas')), url('', include(preferencias_urls, namespace='preferencias')))