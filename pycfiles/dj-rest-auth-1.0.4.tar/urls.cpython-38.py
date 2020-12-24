# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/circleci/project/dj_rest_auth/urls.py
# Compiled at: 2020-03-01 00:55:24
# Size of source mod 2**32: 901 bytes
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, UserDetailsView
from django.conf.urls import url
urlpatterns = [
 url('^password/reset/$', (PasswordResetView.as_view()), name='rest_password_reset'),
 url('^password/reset/confirm/$', (PasswordResetConfirmView.as_view()), name='rest_password_reset_confirm'),
 url('^login/$', (LoginView.as_view()), name='rest_login'),
 url('^logout/$', (LogoutView.as_view()), name='rest_logout'),
 url('^user/$', (UserDetailsView.as_view()), name='rest_user_details'),
 url('^password/change/$', (PasswordChangeView.as_view()), name='rest_password_change')]