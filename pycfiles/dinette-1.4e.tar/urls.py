# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/forum/urls.py
# Compiled at: 2013-07-02 04:51:32
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', (
 '^forum/', include('dinette.urls')), (
 '^accounts/', include('accounts.urls')), (
 '^admin/', include(admin.site.urls)))
if settings.DEBUG or getattr(settings, 'SERVE_MEDIA', False):
    urlpatterns += patterns('django.views.static', (
     '^site_media/(?P<path>.*)$', 'serve',
     {'document_root': settings.MEDIA_ROOT, 
        'show_indexes': True}))