# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/urls.py
# Compiled at: 2017-04-24 04:30:52
# Size of source mod 2**32: 2295 bytes
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from mote import views, api
app_name = 'mote'
urlpatterns = [
 url('^$', views.HomeView.as_view(), name='home'),
 url('^project/partial/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/(?P<variation>[\\w-]+)/$', views.VariationPartialView.as_view(), name='variation-partial'),
 url('^project/iframe/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/(?P<variation>[\\w-]+)/$', views.VariationIframeView.as_view(), name='variation-iframe'),
 url('^project/partial/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/$', views.ElementPartialView.as_view(), name='element-partial'),
 url('^project/iframe/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/$', views.ElementIframeView.as_view(), name='element-iframe'),
 url('^project/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/$', views.ElementIndexView.as_view(), name='element-index'),
 url('^project/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/$', views.PatternView.as_view(), name='pattern'),
 url('^project/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/$', views.AspectView.as_view(), name='aspect'),
 url('^project/(?P<project>[\\w-]+)/$', views.ProjectView.as_view(), name='project')]
api_urlpatterns = [
 url('^api/project/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/(?P<variation>[\\w-]+)/$', api.VariationDetail.as_view(), name='api-variation-detail'),
 url('^api/project/(?P<project>[\\w-]+)/(?P<aspect>[\\w-]+)/(?P<pattern>[\\w-]+)/(?P<element>[\\w-]+)/$', api.ElementDetail.as_view(), name='api-element-detail'),
 url('^api/multiplex/$', api.Multiplex.as_view(), name='api-multiplex')]
urlpatterns = urlpatterns + format_suffix_patterns(api_urlpatterns)