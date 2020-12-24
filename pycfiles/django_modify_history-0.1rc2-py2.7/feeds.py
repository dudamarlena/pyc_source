# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modify_history/feeds.py
# Compiled at: 2011-06-10 23:28:22
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
lazy_reverse = lazy(reverse, str)
from models import Timeline

class LatestTimelineFeed(Feed):
    title = '最近の更新 - Kawaz.tk'
    description = '札幌ゲーム製作者コミュニティKawazの全体の更新情報'
    link = lazy_reverse('history-timeline-feeds')

    def items(self):
        queryset = Timeline.objects.order_by('-created_at')
        return queryset[:50]

    def item_title(self, item):
        return item.get_message()

    def item_description(self, item):
        return item.get_message()

    def item_link(self, item):
        return item.get_absolute_url()