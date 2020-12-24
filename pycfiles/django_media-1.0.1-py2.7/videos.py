# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/media/urls/videos.py
# Compiled at: 2012-04-05 17:42:51
from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from media.models import Video, VideoSet
urlpatterns = patterns('', url('^$', view=ListView.as_view(model=Video), name='video_list'), url('^(?P<slug>[-\\w]+)/$', view=DetailView.as_view(model=Video), name='video_detail'), url('^sets/$', view=ListView.as_view(model=VideoSet), name='video_set_list'), url('^sets/(?P<slug>[-\\w]+)/$', view=DetailView.as_view(model=VideoSet), name='video_set_detail'))