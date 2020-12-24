# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svdgraaf/Projects/nl.focusmedia/lib/python2.7/site-packages/eloqua/urls.py
# Compiled at: 2013-03-01 08:54:58
from django.conf.urls.defaults import patterns, include, url
from .views import LandingPageView
urlpatterns = patterns('', url('^(?P<pk>[0-9]+)-?(?P<slug>[a-zA-Z0-9-_]+)?/?$', LandingPageView.as_view(), name='eloqua:landing_page'))