# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/exceptions.py
# Compiled at: 2016-12-08 10:01:20
# Size of source mod 2**32: 421 bytes
from tornado.web import HTTPError as _HTTPError

class HTTPError(_HTTPError):
    __doc__ = "\n    Custom HTTPError class\n    Expands kwargs with body argument\n    Usage:\n    raise HTTPError(400, b'Something bad happened')\n    "

    def __init__(self, status_code=500, log_message=None, *args, **kwargs):
        super(HTTPError, self).__init__(status_code, log_message, *args, **kwargs)
        self.body = kwargs.get('body')