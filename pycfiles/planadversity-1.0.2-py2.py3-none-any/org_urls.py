# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/org_urls.py
# Compiled at: 2014-07-14 11:38:21
from django.conf.urls import patterns, url
from .views import OpportunityDetailView, ProjectListView, ProjectDetailView, DashboardView, ProfileUpdateView, ProjectCreateView, OpportunityVolunteerView, OpportunityUnVolunteerView, OrganizationCreateView
urlpatterns = patterns('', url('^(?P<org_id>[\\d]+)/projects/(?P<slug>[-\\w]+)/opportunities/$', view=ProjectDetailView.as_view(), name='project-detail'), url('^(?P<org_id>[\\d]+)/projects/add/(?P<slug>[-\\w]+)/$', view=ProjectCreateView.as_view(), name='project-create'), url('^(?P<org_id>[\\d]+)/projects/$', view=ProjectListView.as_view(), name='project-list'), url('^(?P<org_id>[\\d]+)/dashboard/edit-profile/$', view=ProfileUpdateView.as_view(), name='profile-update'), url('^(?P<org_id>[\\d]+)/dashboard/$', view=DashboardView.as_view(), name='dashboard'))