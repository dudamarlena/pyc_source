# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/api/urls-like.py
# Compiled at: 2018-11-05 07:19:14
from django.conf.urls import url
from .views import LikeListAPIView, LikeDetailAPIView, LikeReviewSetAPIView
urlpatterns = [
 url('^$', LikeListAPIView.as_view(), name='list'),
 url('^set/$', LikeReviewSetAPIView.as_view(), name='set'),
 url('^(?P<like_id>\\d+)/$', LikeDetailAPIView.as_view(), name='detail')]