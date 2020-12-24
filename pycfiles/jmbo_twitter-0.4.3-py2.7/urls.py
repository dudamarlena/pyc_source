# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_twitter/urls.py
# Compiled at: 2014-12-17 03:04:08
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('', url('^feed/(?P<slug>[\\w-]+)/$', 'jmbo.views.object_detail', name='feed_object_detail'), url('^search/(?P<slug>[\\w-]+)/$', 'jmbo.views.object_detail', name='search_object_detail'))