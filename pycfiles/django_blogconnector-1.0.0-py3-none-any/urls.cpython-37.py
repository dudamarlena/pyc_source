# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\vryhofa\workspace\django-wordpress-rss\htdocs\django_blogconnector\urls.py
# Compiled at: 2019-05-13 14:45:31
# Size of source mod 2**32: 377 bytes
from django.conf.urls import url
from .views import BlogCategoryView, BlogHomeView, BlogPostView
urlpatterns = [
 url('post/(?P<post_slug>[a-z0-9_\\-]+)/', (BlogPostView.as_view()), name='blog_post'),
 url('category/(?P<category_slug>[a-z0-9_\\-]+)/', (BlogCategoryView.as_view()), name='blog_category'),
 url('^$', (BlogHomeView.as_view()), name='blog_home')]