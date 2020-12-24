# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/sitemaps.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 1048 bytes
from django.contrib.sitemaps import Sitemap
from authors.models import Author
from content.models import Article, Case, Event, Issue, Topic

class AuthorSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.5

    def items(self):
        return Author.objects.all()


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def last_mod(self, obj):
        return obj.date_label


class TopicSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Topic.objects.all()


class IssueSitemap(Sitemap):
    chagefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Issue.objects.all()


class EventSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Event.objects.all()


class CaseSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Case.objects.all()

    def last_mod(self, obj):
        return obj.date_label