# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangotags\src\djangotags\rest_api\urls.py
# Compiled at: 2020-04-02 22:13:46
# Size of source mod 2**32: 581 bytes
from django.conf.urls import re_path, include
from djangotags.rest_api import viewsets
urlpatterns = [
 re_path('^tag/all/$', (viewsets.TagListViewSet.as_view()), name='tag_list_viewset'),
 re_path('^tag/(?P<tag_slug>[\\w-]+)/$', (viewsets.TagRetrieveViewSet.as_view()), name='tag_retrieve_viewset'),
 re_path('^tag/(?P<tag_slug>[\\w-]+)/update/$', (viewsets.TagUpdateViewSet.as_view()), name='tag_update_viewset'),
 re_path('^tag/(?P<tag_slug>[\\w-]+)/delete/$', (viewsets.TagDestroyViewSet.as_view()), name='tag_destroy_viewset')]