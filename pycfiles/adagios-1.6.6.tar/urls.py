# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/urls.py
# Compiled at: 2018-05-16 10:07:32
from django.conf.urls import url, patterns, include
from adagios import settings
from django.views.static import serve
urlpatterns = patterns('', url('^$', 'adagios.views.index', name='home'), url('^403', 'adagios.views.http_403'), url('^objectbrowser', include('adagios.objectbrowser.urls')), url('^status', include('adagios.status.urls')), url('^bi', include('adagios.bi.urls')), url('^misc', include('adagios.misc.urls')), url('^pnp', include('adagios.pnp.urls')), url('^media(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), url('^rest', include('adagios.rest.urls')), url('^contrib', include('adagios.contrib.urls')), url('^jsi18n/$', 'django.views.i18n.javascript_catalog'))
if settings.DEBUG:
    urlpatterns += patterns('', url('^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}, name='media'))