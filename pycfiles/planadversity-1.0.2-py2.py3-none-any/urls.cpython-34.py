# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/planadversity/planadversity/apps/meditations/urls.py
# Compiled at: 2016-02-24 09:37:34
# Size of source mod 2**32: 1107 bytes
from django.conf.urls import url
from .views import MeditationListView, MeditationDetailView, MeditationListJSONView, HomepageView, ResponseListView, ResponseDetailView, ResponseCreateView
urlpatterns = [
 url('^meditations.json', view=MeditationListJSONView.as_view(), name='meditation-list-json'),
 url('^meditations/(?P<slug>[-\\w]+)/', view=MeditationDetailView.as_view(), name='meditation-detail'),
 url('^meditations/$', view=MeditationListView.as_view(), name='meditation-list'),
 url('^responses/create/$', view=ResponseCreateView.as_view(), name='response-create'),
 url('^responses/(?P<slug>[-\\w\\d]+)/', view=ResponseDetailView.as_view(), name='response-detail'),
 url('^responses/$', view=ResponseListView.as_view(), name='response-list'),
 url('^$', view=HomepageView.as_view(), name='homepage')]