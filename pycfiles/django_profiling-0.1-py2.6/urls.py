# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/dprofiling/tests/urls.py
# Compiled at: 2013-05-14 10:51:04
from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from dprofiling.tests import views
urlpatterns = patterns('', url('^a/$', views.HelloWorld.as_view()), url('^b/$', views.HelloWorld.as_view()), url('^c/$', views.HelloWorld.as_view()), url('^d/$', views.ExceptionView.as_view()), url('^e/$', views.NotFoundView.as_view()), url('^f/$', RedirectView.as_view(url='/a/')))