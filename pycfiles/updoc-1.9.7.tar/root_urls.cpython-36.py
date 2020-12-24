# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Updoc/updoc/root_urls.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 833 bytes
from django.conf.urls import include, url
from updoc import views
from updoc.feeds import LastDocsFeed, FavoritesFeed, KeywordFeed, MostViewedDocsFeed
__author__ = 'Matthieu Gallet'
urls = [
 url('^rss/favorites/(?P<root_id>\\d+)/', (FavoritesFeed()), name='favorites'),
 url('^rss/keywords/(?P<kw>[^/]+)/', (KeywordFeed()), name='keywords'),
 url('^rss/most_viewed/', (MostViewedDocsFeed()), name='most_viewed_feed'),
 url('^rss/last_docs/', (LastDocsFeed()), name='last_docs_rss'),
 url('^updoc/', include('updoc.urls', namespace='updoc')),
 url('^upload\\.html$', (views.upload), name='upload'),
 url('^upload_doc_progress\\.html$', (views.upload_doc_progress), name='upload_doc_progress'),
 url('^upload_api/', (views.upload_doc_api), name='upload_doc_api')]