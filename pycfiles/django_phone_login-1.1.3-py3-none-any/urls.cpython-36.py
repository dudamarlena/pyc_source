# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ray/Work/Rumor/django-phone-login/phone_login/urls.py
# Compiled at: 2017-08-01 15:46:19
# Size of source mod 2**32: 227 bytes
from django.conf.urls import url
from .views import GenerateOTP, ValidateOTP
urlpatterns = [
 url('^generate/$', (GenerateOTP.as_view()), name='generate'),
 url('^validate/$', (ValidateOTP.as_view()), name='validate')]