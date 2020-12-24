# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahernp/code/django-ahernp/ahernp/dmcm/edit/urls.py
# Compiled at: 2016-01-22 06:27:12
from __future__ import absolute_import
from django.conf.urls import url
from .views import PageCreateView, PageListView, PageUpdateView
urlpatterns = [
 url(regex='^$', view=PageListView.as_view(), name='edit'),
 url(regex='^page/$', view=PageListView.as_view(), name='list_pages'),
 url(regex='^page/add/$', view=PageCreateView.as_view(), name='add_page'),
 url(regex='^(?P<slug>[-\\w]+)/$', view=PageUpdateView.as_view(), name='update_page')]