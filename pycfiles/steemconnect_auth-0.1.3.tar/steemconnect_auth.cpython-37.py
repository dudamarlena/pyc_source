# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\AppData\Local\Temp\pip-install-9f4wujyx\steemconnect-auth\steemconnect_auth\middleware\steemconnect_auth.py
# Compiled at: 2019-05-20 22:11:00
# Size of source mod 2**32: 267 bytes
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class SteemConnectAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.steemconnect_auth = settings.STEEMCONNECT_AUTH_CONFIGS