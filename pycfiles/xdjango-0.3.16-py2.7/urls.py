# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdjango/urls.py
# Compiled at: 2016-06-20 12:45:24
from django.conf.urls import url, include
from rest_framework import routers
from xdjango.contrib.auth import views
router = routers.DefaultRouter()
router.register('users', views.UserEmailViewSet)
urlpatterns = [
 url('^', include(router.urls)),
 url('^sessions/$', views.SessionAPIView.as_view()),
 url('^preset/(?P<user_id>\\d+)/(?P<token>\\w+)', views.ResetView.as_view())]