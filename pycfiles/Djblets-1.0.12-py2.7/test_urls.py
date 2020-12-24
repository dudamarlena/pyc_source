# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/feedview/test_urls.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import os
from django.conf.urls import url
from djblets.feedview.views import view_feed
FEED_URL = b'file://%s/testdata/sample.rss' % os.path.dirname(__file__)
urlpatterns = [
 url(b'^feed/$', view_feed, {b'template_name': b'feedview/feed-page.html', 
    b'url': FEED_URL}),
 url(b'^feed-inline/$', view_feed, {b'template_name': b'feedview/feed-inline.html', 
    b'url': FEED_URL}),
 url(b'^feed-error/$', view_feed, {b'template_name': b'feedview/feed-inline.html', 
    b'url': b'http://example.fake/dummy.rss'})]