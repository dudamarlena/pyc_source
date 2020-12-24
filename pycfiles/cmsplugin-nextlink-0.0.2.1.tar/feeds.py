# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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