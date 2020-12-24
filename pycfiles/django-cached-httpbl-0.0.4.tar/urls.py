# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacOSExt/Projects/django-apps/django_cached_httpbl/docs/example_app/example_app/urls.py
# Compiled at: 2016-04-05 07:30:24
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
urlpatterns = patterns('', url('^$', TemplateView.as_view(template_name='index.html')))