# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/richcomments/urls.py
# Compiled at: 2011-09-15 07:14:57
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('richcomments.views', url('^list/(?P<content_type>[\\w-]+)/(?P<id>\\d+)$', 'list', name='render_comment_list'))