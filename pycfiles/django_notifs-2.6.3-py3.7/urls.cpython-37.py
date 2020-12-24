# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/urls.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 285 bytes
"""Frontend urls."""
from django.conf.urls import url
from . import views
app_name = 'notifications'
urlpatterns = [
 url('^$', (views.NotificationsView.as_view()), name='notifications_view'),
 url('^generate-notification/$', views.GenerateNotification.as_view())]