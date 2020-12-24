# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: rest_auth/urls.py
# Compiled at: 2017-08-26 14:01:07
from django.conf.urls import url
from rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
urlpatterns = [
 url('^password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
 url('^password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
 url('^login/$', LoginView.as_view(), name='rest_login'),
 url('^logout/$', LogoutView.as_view(), name='rest_logout'),
 url('^user/$', UserDetailsView.as_view(), name='rest_user_details'),
 url('^password/change/$', PasswordChangeView.as_view(), name='rest_password_change')]