# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/../dorrie/urls.py
# Compiled at: 2012-01-23 15:46:01
from django.conf import settings
from django.conf.urls.defaults import *
from comps import views
urlpatterns = patterns('', (
 '^$', views.home), (
 '^packages/$', views.packages), (
 '^select/$', views.select), (
 '^build/$', views.build), (
 '^process/$', views.process), (
 '^tail/$', views.tail))
if settings.STATIC_SERVE:
    urlpatterns += patterns('', (
     '^static/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))