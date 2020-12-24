# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/urls.py
# Compiled at: 2015-04-28 15:32:14
from django.conf import settings
from django.conf.urls import patterns, url
from jmbo.urls import v1_api
from jmbo.views import ObjectDetail
from music.api import TrackResource
v1_api.register(TrackResource())
urlpatterns = patterns('', url('^track/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='track_object_detail'), url('^album/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='album_object_detail'), url('^audioembed/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='audioembed_object_detail'), url('^trackcontributor/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='trackcontributor_object_detail'))