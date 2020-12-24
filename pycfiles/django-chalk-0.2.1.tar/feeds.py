# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/feeds.py
# Compiled at: 2013-08-20 17:44:47
from datetime import datetime, time
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from .models import Article
from .settings import FEED_TITLE, FEED_DESCRIPTION

class ArticleRssFeed(Feed):

    def title(self):
        return FEED_TITLE

    def description(self):
        return FEED_DESCRIPTION

    def link(self):
        return reverse('list_articles')

    def items(self):
        return Article.objects.filter(published=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt_html

    def item_pubdate(self, item):
        return datetime.combine(item.publication_date, time())

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_author_email(self, item):
        return item.author.email


class ArticleAtomFeed(ArticleRssFeed):
    feed_type = Atom1Feed
    subtitle = ArticleRssFeed.description