# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/site_basics/urls.py
# Compiled at: 2013-03-08 03:41:18
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView, RedirectView
from robots_txt.views import RobotsTextView
from views import page_404, page_500
import conf
urlpatterns = patterns('', url('', include('favicon.urls')), url('^robots.txt$', RobotsTextView.as_view(template_name=conf.ROBOTS_TEMPLATE), name='site_robots_txt'), url('^test_page_404/$', page_404, name='page_404'), url('^test_page_500/$', page_500, name='page_500'))