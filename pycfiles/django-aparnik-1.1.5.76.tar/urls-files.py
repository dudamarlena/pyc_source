# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/api/urls-files.py
# Compiled at: 2019-02-20 06:26:52
from django.conf.urls import url, include
from .views import CourseFileListAPIView, CourseFileCreateAPIView
urlpatterns = [
 url('^$', CourseFileListAPIView.as_view(), name='list'),
 url('^create/$', CourseFileCreateAPIView.as_view(), name='create')]