# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/urls.py
# Compiled at: 2020-03-04 05:34:56
# Size of source mod 2**32: 143 bytes
from django.urls import path
from drf_social.view import SocialLoginView
urlpatterns = [
 path('social/login', SocialLoginView.as_view())]