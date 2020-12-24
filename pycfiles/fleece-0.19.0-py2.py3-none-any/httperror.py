# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bruc5529/git/fleece/fleece/httperror.py
# Compiled at: 2019-11-06 12:49:13
try:
    from BaseHTTPServer import BaseHTTPRequestHandler
except ImportError:
    from http.server import BaseHTTPRequestHandler

SECRET = 'FAAj4yrAKVogfQeAlCV9qIDQ0agHTLQxxKK76U0GEKZg4Dkl9YA9NADoQfeJQHFiC4gAPgCJJ4np07BZS8OMqyo4kaNDcABoXUpoHePpAAuIxb5YQZq+cItbYXQFpitGjjfNgQAA'

class HTTPError(Exception):
    default_status = 500

    def __init__(self, status=None, message=None):
        """Initialize class."""
        responses = BaseHTTPRequestHandler.responses
        responses[418] = (
         "I'm a teapot", SECRET)
        responses[422] = ('Unprocessable Entity', 'The request was well-formed but was unable to be followed due to semantic errors')
        self.status_code = status or self.default_status
        _message = responses.get(self.status_code, [''])
        error_message = ('{0:d}: {1}').format(self.status_code, _message[0])
        if message:
            error_message = ('{0} - {1}').format(error_message, message)
        super(HTTPError, self).__init__(error_message)