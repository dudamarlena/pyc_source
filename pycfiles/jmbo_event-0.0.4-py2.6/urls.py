# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/event/urls.py
# Compiled at: 2012-05-07 06:37:42
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('event.views', url('^list/$', 'object_list', name='event_entryitem_list'), url('^(?P<slug>[\\w-]+)/$', 'object_detail', name='event_object_detail'))