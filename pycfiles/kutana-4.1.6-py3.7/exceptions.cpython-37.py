# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/exceptions.py
# Compiled at: 2020-04-18 16:07:01
# Size of source mod 2**32: 221 bytes


class RequestException(Exception):

    def __init__(self, backend, request, response, error=None):
        self.backend = backend
        self.request = request
        self.response = response
        self.error = error