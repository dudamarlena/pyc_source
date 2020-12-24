# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/urls.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 697 bytes
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from ovp_users import views
router = routers.DefaultRouter()
router.register('users', views.UserResourceViewSet, 'user')
router.register('users/recovery-token', views.RecoveryTokenViewSet, 'recovery-token')
router.register('users/recover-password', views.RecoverPasswordViewSet, 'recover-password')
router.register('users/send-message', views.UserMessageViewSet, 'send-message')
router.register('public-users', views.PublicUserResourceViewSet, 'public-users')
urlpatterns = [
 url('^', include(router.urls)),
 url('^api-token-auth/', obtain_jwt_token)]