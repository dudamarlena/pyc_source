# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/honey/project_urls.py
# Compiled at: 2016-08-07 14:13:35
# Size of source mod 2**32: 1626 bytes
from django.conf.urls import url
from honey import views as honey_views
urlpatterns = [
 url('^projects/add/', view=honey_views.ProjectCreateView.as_view(), name='project-create'),
 url('^projects/(?P<slug>[-\\w]+)/edit/', view=honey_views.ProjectUpdateView.as_view(), name='project-update'),
 url('^projects/(?P<slug>[-\\w]+)/join/', view=honey_views.ProjectJoinView.as_view(), name='project-join'),
 url('^projects/(?P<slug>[-\\w]+)/leave/', view=honey_views.ProjectLeaveView.as_view(), name='project-leave'),
 url('^projects/(?P<slug>[-\\w]+)/buzz/create/', view=honey_views.BuzzCreateView.as_view(), name='buzz-create'),
 url('^projects/(?P<project_slug>[-\\w]+)/buzz/(?P<slug>[-\\w]+)/', view=honey_views.BuzzDetailView.as_view(), name='buzz-detail'),
 url('^projects/(?P<project_slug>[-\\w]+)/commit/(?P<slug>[-\\w]+)/', view=honey_views.ProjectCommitDetailView.as_view(), name='commit-detail'),
 url('^projects/(?P<slug>[-\\w]+)/link/create/', view=honey_views.LinkCreateView.as_view(), name='link-create'),
 url('^projects.json', view=honey_views.ProjectListJSONView.as_view(), name='project-list-json'),
 url('^projects/(?P<slug>[-\\w]+)/', view=honey_views.ProjectDetailView.as_view(), name='project-detail'),
 url('^projects/$', view=honey_views.ProjectListView.as_view(), name='project-list')]