# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/competition/urls.py
# Compiled at: 2010-08-04 03:48:25
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('competition.views', url('^list/$', 'object_list', name='competition_object_list'), url('^info/$', 'preferences_detail', name='competition_preferences_detail'), url('^(?P<slug>[\\w-]+)/$', 'object_detail', name='competition_object_detail'))