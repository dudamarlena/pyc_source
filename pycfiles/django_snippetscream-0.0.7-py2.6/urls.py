# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snippetscream/tests/urls.py
# Compiled at: 2011-09-19 04:39:10
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('', url('^some/url/$', 'app.views.view'), url('^some/other/url/$', 'app.views.other.view', name='this_is_a_named_view'))