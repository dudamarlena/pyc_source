# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/tests/urls.py
# Compiled at: 2018-03-27 03:51:51
from django.conf.urls import include, url
from layers.tests import views
urlpatterns = [
 url('^normal-view/$', views.NormalView.as_view(), name='normal-view'),
 url('^web-only-view/$', views.WebOnlyView.as_view(), name='web-only-view')]