# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modify_history/urls.py
# Compiled at: 2011-06-10 23:28:22
from django.conf.urls.defaults import *
from models import Timeline
from feeds import LatestTimelineFeed
dict_info = {'queryset': Timeline.objects.order_by('-created_at'), 
   'paginate_by': 100}
urlpatterns = patterns('django.views.generic.list_detail', (
 '^$', 'object_list', dict_info, 'history-timeline-list'))
urlpatterns += patterns('django.contrib.syndication.views', (
 '^feeds/$', LatestTimelineFeed(), {}, 'history-timeline-feeds'))