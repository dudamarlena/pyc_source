# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halit/pytr/pytrorg/src/urls.py
# Compiled at: 2012-09-09 13:52:32
from django.conf.urls import patterns, include, url
from django.contrib import admin
from settings import MEDIA_ROOT, STATIC_ROOT
from blog.feeds import RSS_URLS
from blog.sitemaps import SITEMAPS_URLS
from sources.feeds import SOURCES_RSS_URLS
from sources.sitemaps import SOURCES_SITEMAPS_URLS
admin.autodiscover()
urlpatterns = patterns('', url('^$', 'blog.views.blogHome', name='bloghome'), url('^admin/', include(admin.site.urls)), (
 '^blog/', include('blog.urls', namespace='blog', app_name='blog')), (
 '^kaynak/', include('sources.urls', namespace='sources', app_name='sources')), (
 '^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}), (
 '^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}))
urlpatterns += RSS_URLS
urlpatterns += SITEMAPS_URLS
urlpatterns += SOURCES_RSS_URLS
urlpatterns += SOURCES_SITEMAPS_URLS