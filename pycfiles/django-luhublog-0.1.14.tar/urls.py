# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/urls.py
# Compiled at: 2015-10-22 10:51:06
from django.conf.urls import include, patterns, url
from . import views
from luhublog.feed import BlogFeed
urlpatterns = patterns('', url('^$', views.EntryListView.as_view(), name='luhublog-list'), url('^feed/$', BlogFeed(), name='luhublog-feed'), url('^(?P<slug>[\\w-]+)/$', views.EntryDetailView.as_view(), name='luhublog-detail'))