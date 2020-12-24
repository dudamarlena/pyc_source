# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/staticblog-bak/urls.py
# Compiled at: 2012-10-05 07:52:59
from django.conf.urls import patterns
urlpatterns = patterns('staticblog.views', ('^$', 'archive'), ('^([\\-\\w]+)$', 'render_post'), ('^git/receive',
                                                                                                 'handle_hook'))