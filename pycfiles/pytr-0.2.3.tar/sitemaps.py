# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halit/pytr/pytrorg/src/sources/sitemaps.py
# Compiled at: 2012-09-09 13:53:01
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.conf.urls.defaults import patterns, url
from sources.models import Sources, Categories
posts_dict = {'queryset': Sources.objects.order_by('-created').filter(isonline=True), 
   'date_field': 'created'}
categories_dict = {'queryset': Categories.objects.all()}
sitemaps = {'posts': GenericSitemap(posts_dict, priority=0.5), 
   'categories': GenericSitemap(categories_dict, priority=1)}
SOURCES_SITEMAPS_URLS = patterns('django.contrib.sitemaps.views', url('^sitemap-sources\\.xml$', 'sitemap', {'sitemaps': sitemaps}))