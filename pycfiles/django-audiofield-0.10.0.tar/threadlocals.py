# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/middleware/threadlocals.py
# Compiled at: 2018-01-28 10:05:32
from django.utils.deprecation import MiddlewareMixin
import threading
_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)


class ThreadLocals(MiddlewareMixin):
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    """

    def process_request(self, request):
        _thread_locals.request = request