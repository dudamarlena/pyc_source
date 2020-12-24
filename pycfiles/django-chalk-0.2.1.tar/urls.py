# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/urls.py
# Compiled at: 2013-08-22 13:48:31
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .feeds import ArticleAtomFeed, ArticleRssFeed
from .views import ArticleView, ArticleList
urlpatterns = patterns('', url('^$', ArticleList.as_view(), name='list_articles'), url('^feed/$', TemplateView.as_view(template_name='chalk/feed_list.html'), name='list_feeds'), url('^feed/rss/$', ArticleRssFeed(), name='rss_feed'), url('^feed/atom/$', ArticleAtomFeed(), name='atom_feed'), url('^(?P<slug>[\\w-]+)/$', ArticleView.as_view(), name='view_article'))