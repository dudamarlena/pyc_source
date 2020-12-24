# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/urls.py
# Compiled at: 2014-04-04 10:09:51
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
urlpatterns = patterns('whatsnew.views', url('^test/', TemplateView.as_view(template_name='whatsnew/test.html'), name='whatsnew-test'))