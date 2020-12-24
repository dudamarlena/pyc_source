# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\urls\password.py
# Compiled at: 2019-12-21 15:55:52
# Size of source mod 2**32: 606 bytes
import django.contrib.auth as auth_views
from django.conf.urls import url
urlpatterns = [
 url('^password/reset/$', (auth_views.PasswordResetView.as_view()), name='password_reset'),
 url('^password/reset/done/$', (auth_views.PasswordResetDoneView.as_view()), name='password_reset_done'),
 url('^reset/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', (auth_views.PasswordResetConfirmView.as_view()),
   name='password_reset_confirm'),
 url('^reset/done/$', (auth_views.PasswordResetCompleteView.as_view()), name='password_reset_complete')]