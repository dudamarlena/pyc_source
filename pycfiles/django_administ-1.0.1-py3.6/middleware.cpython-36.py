# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\administ\middleware.py
# Compiled at: 2017-10-18 05:42:28
# Size of source mod 2**32: 381 bytes
from django.conf import settings
from django.http import HttpResponseServerError
from django.utils.deprecation import MiddlewareMixin

class AdministMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        ip = request.META['REMOTE_ADDR']
        if ip not in settings.ADMINIST_ALLOWED_IP:
            return HttpResponseServerError()