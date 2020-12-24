# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/voice/urls.py
# Compiled at: 2011-09-23 16:00:15
from django.conf.urls.defaults import *
urlpatterns = patterns('voice', url('^static/(?P<path>.*)$', 'views.static_media', name='voice-media'), url('^$', 'views.index', name='voice-index'), url('^features/(?P<feature_id>\\d+)$', 'views.feature', name='voice-feature'), url('^features/new/', 'views.new_feature', name='voice-new-feature'), url('^admin/', 'views.admin', name='voice-admin'))