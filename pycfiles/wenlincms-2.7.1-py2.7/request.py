# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/request.py
# Compiled at: 2015-08-11 07:38:42
from __future__ import unicode_literals
import threading
_thread_local = threading.local()

def current_request():
    """
    Retrieves the request from the current thread.
    """
    return getattr(_thread_local, b'request', None)


class CurrentRequestMiddleware(object):
    """
    Stores the request in the current thread for global access.
    """

    def process_request(self, request):
        _thread_local.request = request