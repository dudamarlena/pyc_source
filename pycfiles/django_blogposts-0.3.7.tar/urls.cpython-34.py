# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/urls.py
# Compiled at: 2018-08-06 07:29:24
# Size of source mod 2**32: 717 bytes
from django.conf.urls import url, include
from django.conf import settings
from .views import PostsListView, PostsDetailView
__author__ = 'spi4ka'
urlpatterns = [
 url('^$', PostsListView.as_view(), name='django-blogposts-list'),
 url('^category/(?P<pk>\\d+)/(?P<slug>[^\\.]+)/$', PostsListView.as_view(), name='django-category-blogposts-list'),
 url('^(?P<pk>\\d+)/(?P<slug>[^\\.]+)/$', PostsDetailView.as_view(), name='django-blogposts-detail')]
if 'rest_framework' in settings.INSTALLED_APPS:
    urlpatterns += [
     url('^api/', include('django_blogposts.rest.urls'))]