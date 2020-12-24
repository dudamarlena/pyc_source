# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/middleware.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from sentry.middleware.sudo import SudoMiddleware as BaseSudoMiddleware

class BrokenRequestMiddleware(object):

    def process_request(self, request):
        raise ImportError('request')


class BrokenResponseMiddleware(object):

    def process_response(self, request, response):
        raise ImportError('response')


class BrokenViewMiddleware(object):

    def process_view(self, request, func, args, kwargs):
        raise ImportError('view')


class SudoMiddleware(BaseSudoMiddleware):

    def has_sudo_privileges(self, request):
        return True