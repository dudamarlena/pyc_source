# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halit/pytr/pytrorg/src/sources/feeds.py
# Compiled at: 2012-09-09 13:50:41
from django.contrib.syndication.views import Feed
from django.conf.urls.defaults import patterns, url
from django.shortcuts import get_object_or_404
from sources.models import Sources

class LastSources(Feed):
    title = 'Python Turkiye - Kaynaklar'
    link = '/'
    description = 'Python Turkiye.Turkce Python Programlama Dili Kaynaklari ve Dersleri'

    def items(self):
        return Sources.objects.order_by('-created').filter(isonline=True)[:5]

    def item_title(self, item):
        return item.sef_title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.created


SOURCES_RSS_URLS = patterns('', url('^rss/sources$', LastSources()))