# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/competition/urls.py
# Compiled at: 2013-09-27 03:42:43
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('competition.views', url('^(?P<slug>[\\w-]+)/$', 'competition_detail', name='competition_object_detail'), url('^(?P<slug>[\\w-]+)/$', 'competition_detail', name='competition-detail'), url('^(?P<slug>[\\w-]+)/terms/$', 'competition_terms', name='competition-terms'))