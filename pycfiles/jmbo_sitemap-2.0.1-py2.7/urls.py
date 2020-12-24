# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_sitemap/urls.py
# Compiled at: 2015-06-02 11:41:58
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from jmbo_sitemap import sitemaps, views
urlpatterns = patterns('', url('^sitemap\\.xml$', views.sitemap, {'sitemaps': sitemaps}, name='sitemap'), url('^sitemap/$', views.SitemapHTMLView.as_view(), name='html-sitemap'))