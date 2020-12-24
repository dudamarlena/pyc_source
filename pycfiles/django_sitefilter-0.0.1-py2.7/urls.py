# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sitefilter/urls.py
# Compiled at: 2012-11-20 08:29:49
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('', url('^manage/(?P<id>\\d+)/$', 'sitefilter.views.manage', name='site_filter'))