# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\logout.py
# Compiled at: 2019-12-16 15:25:11
# Size of source mod 2**32: 289 bytes
from django.http import HttpRequest, HttpResponseRedirect
import django.contrib.auth as user_logout
from django.conf import settings

def logout(request: HttpRequest):
    user_logout(request)
    return HttpResponseRedirect(getattr(settings, 'LOGOUT_REDIRECT', '/'))