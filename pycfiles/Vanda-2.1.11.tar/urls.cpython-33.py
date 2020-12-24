# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/multilang/urls.py
# Compiled at: 2013-02-13 07:19:39
# Size of source mod 2**32: 1715 bytes
import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^admin/', include(admin.site.urls)))
if settings.DEBUG:
    urlpatterns += patterns('', (
     '^statics/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), settings.MEDIA_ROOT).replace('\\', '/')}))
urlpatterns += patterns('', ('^(en|fa)[/]?', 'vanda.apps.multilang.dispatcher.dispatch_url'), ('^$',
                                                                                               'vanda.apps.multilang.dispatcher.dispatch_url'), ('.*',
                                                                                                                                                 'vanda.apps.multilang.dispatcher.dispatch_url'))