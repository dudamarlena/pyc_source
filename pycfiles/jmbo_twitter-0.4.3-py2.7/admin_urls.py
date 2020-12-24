# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_twitter/admin_urls.py
# Compiled at: 2014-08-24 14:48:29
from django.conf.urls.defaults import patterns, url, include
urlpatterns = patterns('', (
 'jmbo_twitter/feed/(?P<id>\\d+)/fetch-force/$',
 'jmbo_twitter.admin_views.feed_fetch_force', {'redirect_to': '/admin/jmbo_twitter/feed'},
 'feed-fetch-force'), (
 '^jmbo_twitter/feed/(?P<id>\\d+)/tweets/$',
 'jmbo_twitter.admin_views.feed_tweets', {},
 'feed-tweets'), (
 'jmbo_twitter/search/(?P<id>\\d+)/fetch-force/$',
 'jmbo_twitter.admin_views.search_fetch_force', {'redirect_to': '/admin/jmbo_twitter/search'},
 'search-fetch-force'), (
 '^jmbo_twitter/search/(?P<id>\\d+)/tweets/$',
 'jmbo_twitter.admin_views.search_tweets', {},
 'search-tweets'))