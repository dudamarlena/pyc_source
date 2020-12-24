# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-navbuilder/navbuilder/urls.py
# Compiled at: 2017-01-25 06:30:30
from django.conf.urls import url
from navbuilder.views import MenuDetailView, MenuListView
urlpatterns = [
 url('^$', MenuListView.as_view(), name='menu-list'),
 url('^(?P<slug>[-\\w]+)/$', MenuDetailView.as_view(), name='menu-detail')]