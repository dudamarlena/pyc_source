# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/selectable_urls.py
# Compiled at: 2014-08-27 19:26:12
from django.conf.urls import *
from selectable import registry
registry.autodiscover()
urlpatterns = patterns('selectable.views', url('^(?P<lookup_name>[-\\w]+)/$', 'get_lookup', name='selectable-lookup'))