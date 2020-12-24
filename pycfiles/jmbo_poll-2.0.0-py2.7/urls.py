# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/poll/urls.py
# Compiled at: 2015-04-29 10:06:47
from django.conf.urls import patterns, url
from jmbo.views import ObjectDetail
from poll.models import Poll
urlpatterns = patterns('', url('^(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='poll_object_detail'), url('^poll-detail-vote/(?P<poll_id>\\d+)/$', 'poll.views.poll_vote', {'template': 'poll/poll_detail.html'}, name='poll-detail-vote'), url('^poll-widget-vote/(?P<poll_id>\\d+)/$', 'poll.views.poll_vote', {'template': 'poll/poll_widget.html'}, name='poll-widget-vote'))