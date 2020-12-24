# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/video/urls.py
# Compiled at: 2015-06-24 05:30:26
from django.conf.urls import patterns, include, url
from jmbo.urls import v1_api
from jmbo.views import ObjectDetail
from video.api import VideoResource
v1_api.register(VideoResource())
urlpatterns = patterns('', url('^(?P<category_slug>[\\w-]+)/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='video_categorized_object_detail'), url('^(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='video_object_detail'))