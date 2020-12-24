# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/urls.py
# Compiled at: 2016-09-16 10:02:59
from django.conf.urls import patterns, url
from . import views

def register_in(router):
    router.register('jira', views.JiraServiceViewSet, base_name='jira')
    router.register('jira-service-project-link', views.JiraServiceProjectLinkViewSet, base_name='jira-spl')
    router.register('jira-attachments', views.AttachmentViewSet, base_name='jira-attachments')
    router.register('jira-projects', views.ProjectViewSet, base_name='jira-projects')
    router.register('jira-issues', views.IssueViewSet, base_name='jira-issues')
    router.register('jira-comments', views.CommentViewSet, base_name='jira-comments')


urlpatterns = patterns('', url('^api/jira-webhook-receiver/$', views.WebHookReceiverViewSet.as_view()))