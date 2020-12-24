# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/panya/urls.py
# Compiled at: 2011-05-26 02:47:52
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('panya.views', url('^peek/(?P<slug>[\\w-]+)/$', 'object_peek', name='object_peek'), url('^(?P<category_slug>[\\w-]+)/list/$', 'category_object_list', name='content_category_object_list'), url('^(?P<category_slug>[\\w-]+)/(?P<slug>[\\w-]+)/$', 'category_object_detail', name='content_category_object_detail'))