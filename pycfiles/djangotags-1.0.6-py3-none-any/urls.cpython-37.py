# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangotags\src\djangotags\rest_api\urls.py
# Compiled at: 2020-03-13 02:00:17
# Size of source mod 2**32: 591 bytes
from django.conf.urls import re_path, include
from rest_framework.routers import DefaultRouter
from djangotags.rest_api import viewsets
urlpatterns = [
 re_path('^list/$', (viewsets.TagListViewSet.as_view()), name='tag_list_viewset'),
 re_path('^detail/(?P<tag_slug>[\\w-]+)/$', (viewsets.TagRetrieveViewSet.as_view()), name='tag_retrieve_viewset'),
 re_path('^update/(?P<tag_slug>[\\w-]+)/$', (viewsets.TagUpdateViewSet.as_view()), name='tag_update_viewset'),
 re_path('^delete/(?P<tag_slug>[\\w-]+)/$', (viewsets.TagDestroyViewSet.as_view()), name='tag_destroy_viewset')]