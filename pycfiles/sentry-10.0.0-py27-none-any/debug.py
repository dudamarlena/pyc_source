# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/middleware/debug.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.conf import settings

class NoIfModifiedSinceMiddleware(object):

    def __init__(self):
        if not settings.DEBUG:
            from django.core.exceptions import MiddlewareNotUsed
            raise MiddlewareNotUsed

    def process_request(self, request):
        request.META.pop('HTTP_IF_MODIFIED_SINCE', None)
        return