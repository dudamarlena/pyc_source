# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/workers/urls.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 579 bytes
from django.conf.urls import *
from . import views
urlpatterns = [
 url('^$', (views.index), name='worker-list'),
 url('^launch_worker/$', (views.launch), name='worker-launch'),
 url('^update/(?P<pk>[0-9]+)/$', (views.update), name='worker-update'),
 url('^install/(?P<pk>[0-9]+)/$', (views.install), name='worker-install'),
 url('^terminate/(?P<pk>[0-9]+)/$', (views.terminate), name='worker-terminate'),
 url('^delete/(?P<pk>\\d+)/$', (views.WorkerDelete.as_view()), name='worker-delete'),
 url('^action/$', (views.action), name='worker-bulk-action')]