# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/admin_urls.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from reviewbotext.views import ConfigureUserView, ConfigureView, WorkerStatusView
urlpatterns = patterns(b'', url(b'^$', ConfigureView.as_view(), name=b'reviewbot-configure'), url(b'^user/$', ConfigureUserView.as_view(), name=b'reviewbot-configure-user'), url(b'^worker-status/$', WorkerStatusView.as_view(), name=b'reviewbot-worker-status'))