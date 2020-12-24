# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cameronlowe/Development/django-zencoder/zencoder/urls.py
# Compiled at: 2017-01-17 17:26:08
# Size of source mod 2**32: 388 bytes
from django.conf.urls import patterns, url
urlpatterns = patterns('zencoder.views', url('^new$', 'video', name='video-new'), url('^(?P<video_id>\\d+)$', 'video', name='video-detail'), url('^(?P<video_id>\\d+)/encode$', 'encode'), url('^notify$', 'notify'), url('^embed$', 'embed'), url('^video/(?P<video_id>\\d+)$', 'video_json', name='video-json'))