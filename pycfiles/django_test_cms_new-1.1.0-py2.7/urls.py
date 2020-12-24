# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\django-test-cms-new\urls.py
# Compiled at: 2019-06-25 04:05:06
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^$', views.home, name='home')]