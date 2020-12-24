# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/api/urls-dislike.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 359 bytes
from django.conf.urls import url
from .views import DislikeReviewSetAPIView, DislikeListAPIView, LikeDetailAPIView
app_name = 'reviews'
urlpatterns = [
 url('^$', (DislikeListAPIView.as_view()), name='list'),
 url('^set/$', (DislikeReviewSetAPIView.as_view()), name='set'),
 url('^(?P<like_id>\\d+)/$', (LikeDetailAPIView.as_view()), name='detail')]