# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/article_urls.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 770 bytes
from django.conf.urls import url
from cmsplugin_articles_ai.views import CategoryView
from .views import ArticleListView, ArticleView, TagFilteredArticleView
urlpatterns = [
 url('^tag/(?P<tag>[-_\\w]+)/', TagFilteredArticleView.as_view(), name='tagged_articles'),
 url('^tagged/', TagFilteredArticleView.as_view(), name='tag_filtered_articles'),
 url('^category/(?P<category>[-_\\w]+)/tag/(?P<tag>[-_\\w]+)/', CategoryView.as_view(), name='tagged_articles_in_category'),
 url('^category/(?P<category>[-_\\w]+)/', CategoryView.as_view(), name='articles_in_category'),
 url('^(?P<slug>[-_\\w]+)/', ArticleView.as_view(), name='article'),
 url('^$', ArticleListView.as_view(), name='articles')]