# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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