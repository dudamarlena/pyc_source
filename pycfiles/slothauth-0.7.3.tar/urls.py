# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/urls.py
# Compiled at: 2016-02-04 14:19:15
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import change_email, login, logout, password_reset, profile, signup, passwordless_signup, passwordless_login, AccountViewSet, AuthViewSet
from . import settings
router = DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('accounts/auth', AuthViewSet)
urlpatterns = [
 url('^api/' + settings.API_VERSION + '/', include(router.urls)),
 url('^signup/?', signup, name='signup'),
 url('^login/?', login, name='login'),
 url('^password_reset/?', password_reset, name='password_reset'),
 url('^change_email/?', change_email, name='change_email'),
 url('^profile/?', profile, name='profile'),
 url('^logout/?', logout, name='logout'),
 url('^passwordless_signup/?', passwordless_signup, name='passwordless_signup'),
 url('^passwordless_login/?', passwordless_login, name='passwordless_login')]