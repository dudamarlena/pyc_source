# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesearch/urls.py
# Compiled at: 2015-04-23 11:12:42
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
urlpatterns = patterns('', url('^results/$', TemplateView.as_view(template_name='googlesearch/results.html'), name='googlesearch-results'), url('^cref-cse\\.xml/$', 'googlesearch.views.cref_cse', {}, name='googlesearch-cref-cse'))