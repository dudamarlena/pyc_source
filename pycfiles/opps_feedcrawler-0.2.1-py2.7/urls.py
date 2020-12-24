# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/opps/feedcrawler/urls.py
# Compiled at: 2014-06-23 11:25:49
from django.conf.urls import patterns
from opps.feedcrawler.views import create_post
urlpatterns = patterns('', (
 '^createpost/(?P<post_id>\\d+)$', create_post, {}, 'create_post'))