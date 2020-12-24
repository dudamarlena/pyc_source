# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/feeds.py
# Compiled at: 2017-12-07 19:41:42
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from . import models
from . import settings

class NewsFeed(Feed):
    title = settings.FEED_TITLE
    description = settings.FEED_DESCRIPTION
    title_template = 'cmsplugin_newsplus/feeds/item_title.html'
    description_template = 'cmsplugin_newsplus/feeds/item_description.html'

    @property
    def link(self):
        return reverse('cmsplugin_newsplus:news_archive_index')

    def items(self):
        return models.News.published.all()[:settings.FEED_SIZE]

    def item_url(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date