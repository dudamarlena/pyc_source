# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/post/urls.py
# Compiled at: 2010-08-11 09:10:12
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('post.views', url('^list/$', 'object_list', name='post_object_list'), url('^(?P<slug>[\\w-]+)/$', 'object_detail', name='post_object_detail'))