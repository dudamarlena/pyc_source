# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/flask_limiter/errors.py
# Compiled at: 2019-10-02 22:11:48
# Size of source mod 2**32: 1214 bytes
"""
errors and exceptions
"""
from distutils.version import LooseVersion
from pkg_resources import get_distribution
from six import text_type
from werkzeug import exceptions
werkzeug_exception = None
werkzeug_version = get_distribution('werkzeug').version
if LooseVersion(werkzeug_version) < LooseVersion('0.9'):
    import werkzeug._internal
    werkzeug._internal.HTTP_STATUS_CODES[429] = 'Too Many Requests'
    werkzeug_exception = exceptions.HTTPException
else:
    werkzeug_exception = exceptions.TooManyRequests

class RateLimitExceeded(werkzeug_exception):
    __doc__ = '\n    exception raised when a rate limit is hit.\n    The exception results in ``abort(429)`` being called.\n    '
    code = 429
    limit = None

    def __init__(self, limit):
        self.limit = limit
        if limit.error_message:
            description = limit.error_message if not callable(limit.error_message) else limit.error_message()
        else:
            description = text_type(limit.limit)
        super(RateLimitExceeded, self).__init__(description=description)