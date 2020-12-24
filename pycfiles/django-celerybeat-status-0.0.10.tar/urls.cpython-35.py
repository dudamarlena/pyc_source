# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/workspaces/workspace_django/django-celerybeat-status/celerybeat_status/urls.py
# Compiled at: 2018-01-27 05:47:23
# Size of source mod 2**32: 226 bytes
from django.conf.urls import url
from celerybeat_status.views import PeriodicTasksStatusListView
urlpatterns = [
 url('^periodic-tasks/$', PeriodicTasksStatusListView.as_view(), name='periodic-tasks-status')]