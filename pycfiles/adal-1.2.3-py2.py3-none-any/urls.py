# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/adagios/adagios/urls.py
# Compiled at: 2018-05-16 10:07:32
from django.conf.urls import url, patterns, include
from adagios import settings
from django.views.static import serve
urlpatterns = patterns('', url('^$', 'adagios.views.index', name='home'), url('^403', 'adagios.views.http_403'), url('^objectbrowser', include('adagios.objectbrowser.urls')), url('^status', include('adagios.status.urls')), url('^bi', include('adagios.bi.urls')), url('^misc', include('adagios.misc.urls')), url('^pnp', include('adagios.pnp.urls')), url('^media(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), url('^rest', include('adagios.rest.urls')), url('^contrib', include('adagios.contrib.urls')), url('^jsi18n/$', 'django.views.i18n.javascript_catalog'))
if settings.DEBUG:
    urlpatterns += patterns('', url('^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}, name='media'))