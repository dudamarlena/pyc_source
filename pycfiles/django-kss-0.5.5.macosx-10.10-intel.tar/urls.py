# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/luyu/venv/lib/python2.7/site-packages/django_kss/urls.py
# Compiled at: 2015-02-09 01:11:49
from django.conf.urls import patterns, include, url
from .views import AutoStyleGuideView, FullTemplateStyleGuideView, InlineTemplateStyleGuideView
from . import utils

def make_style_guide_pattern(template_name='styleguide.html'):
    view = AutoStyleGuideView.as_view(template_name=template_name)
    return patterns('', url('^$', view, name='styleguide'), url('^full/(?P<app_name>.*)/(?P<html>.*\\.html)$', FullTemplateStyleGuideView.as_view(), name='prototype'), url('^(?P<app_name>.*)/(?P<html>.*\\.html)/$', InlineTemplateStyleGuideView.as_view(), name='inline_prototype'), url('^(?P<app_name>.*)/(?P<section>.*)/$', view, name='styleguide'), url('^(?P<app_name>.*)/$', view, name='styleguide'))


urlpatterns = make_style_guide_pattern()