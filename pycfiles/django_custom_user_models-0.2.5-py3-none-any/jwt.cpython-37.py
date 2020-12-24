# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\urls\jwt.py
# Compiled at: 2019-12-21 15:55:52
# Size of source mod 2**32: 151 bytes
from django.conf.urls import url
from CustomAuth.views import new_jwt_token
urlpatterns = [
 url('jwt/new', new_jwt_token, name='jwt new')]