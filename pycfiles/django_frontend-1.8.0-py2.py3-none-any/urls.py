# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faustman/Sites/projects/django-frontend/djfrontend/tests/urls.py
# Compiled at: 2014-01-27 16:39:32
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('', url('^$', TemplateView.as_view(template_name='djfrontend/base.html')))
urlpatterns += staticfiles_urlpatterns()