# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme/middleware.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 314 bytes
from threading import local
from django.utils.deprecation import MiddlewareMixin
_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)


class RequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _thread_locals.request = request