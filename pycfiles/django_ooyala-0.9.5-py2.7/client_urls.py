# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ooyala/client_urls.py
# Compiled at: 2011-01-27 11:10:56
from django.conf.urls.defaults import *
urlpatterns = patterns('', (
 '^channel/(?P<object_id>\\d+)/$', 'ooyala.views.channel', {}, 'channel'), (
 '^search/$', 'ooyala.views.search', {}, 'search'), (
 '^$', 'ooyala.views.home', {}, 'home'))