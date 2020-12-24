# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bryan/.virtualenvs/vancouversymphony/lib/python2.6/site-packages/assume/admin_urls.py
# Compiled at: 2010-11-16 05:26:25
from django.conf.urls.defaults import *
urlpatterns = patterns('', url('^auth/user/(\\d+)/assume/$', 'assume.views.assume_user', name='assume_user'))