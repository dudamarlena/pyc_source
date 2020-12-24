# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/urls.py
# Compiled at: 2011-09-19 04:01:13
from django.conf import settings
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('music.views', url('^listen-live/$', 'listen_live', {'object_id': getattr(settings, 'LISTEN_LIVE_AUDIO_EMBED_ID', '-1')}, name='music_listen_live'))