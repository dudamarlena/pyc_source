# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/urls.py
# Compiled at: 2016-09-19 04:59:30
# Size of source mod 2**32: 784 bytes
from django.conf.urls import patterns, url
from .views import TaskListView, TaskDetailView, TaskBulksView, UploadTranslationsView, MessageView, DownloadFileView
urlpatterns = patterns('', url('^/task/$', TaskListView.as_view(), name='transmanager-task-list'), url('^/task/(?P<pk>\\d+)/$', TaskDetailView.as_view(), name='transmanager-task-detail'), url('^/api/task/$', TaskBulksView.as_view(), name='transmanager-task-bulks'), url('^/upload-translations/$', UploadTranslationsView.as_view(), name='transmanager-upload-translations'), url('^/message/$', MessageView.as_view(), name='transmanager-message'), url('^/download-file/(?P<uuid>[a-zA-z0-9-]+)/$', DownloadFileView.as_view(), name='transmanager-download-file'))