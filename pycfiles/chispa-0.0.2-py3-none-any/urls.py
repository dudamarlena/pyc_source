# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/devel/chishop/chishop/urls.py
# Compiled at: 2009-03-17 09:10:16
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('')
if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('django.views', url('%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'static.serve', {'document_root': settings.MEDIA_ROOT}))
urlpatterns += patterns('', url('^admin/doc/', include('django.contrib.admindocs.urls')), url('^admin/(.*)', admin.site.root), url('', include('djangopypi.urls')))