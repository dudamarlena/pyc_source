# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/news/urls.py
# Compiled at: 2014-03-27 09:47:06
from django.conf.urls import patterns, url
urlpatterns = patterns('news.views', url('^$', 'ArticleList', name='articles_list'), url('^(?P<slug>[\\w-]+)/$', 'ArticleDetail', name='articles_detail'))