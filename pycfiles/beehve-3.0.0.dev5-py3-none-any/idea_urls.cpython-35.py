# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/honey/idea_urls.py
# Compiled at: 2016-08-07 14:09:36
# Size of source mod 2**32: 834 bytes
from django.conf.urls import url
from honey import views as honey_views
urlpatterns = [
 url('^ideas/add/', view=honey_views.ProjectIdeaCreateView.as_view(), name='projectidea-create'),
 url('^ideas/(?P<slug>[-\\w]+)/edit/', view=honey_views.ProjectIdeaUpdateView.as_view(), name='projectidea-update'),
 url('^ideas.json', view=honey_views.ProjectIdeaListJSONView.as_view(), name='projectidea-list-json'),
 url('^ideas/(?P<slug>[-\\w]+)/', view=honey_views.ProjectIdeaDetailView.as_view(), name='projectidea-detail'),
 url('^ideas/$', view=honey_views.ProjectIdeaListView.as_view(), name='projectidea-list')]