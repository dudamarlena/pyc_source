# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/errors.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 1626 bytes


class ICError(Exception):
    __doc__ = 'Base error for this module.'

    def __init__(self, resp, content, uri=None):
        self.resp = resp
        self.content = content
        self.uri = uri


class ICNotAuthorizedError(ICError):
    __doc__ = 'The authorization information provided is not correct'


class ICNotFoundError(ICError):
    __doc__ = 'The IonosEnterprise entity was not found'


class ICValidationError(ICError):
    __doc__ = 'The HTTP data provided is not valid'


class ICRateLimitExceededError(ICError):
    __doc__ = 'The number of requests sent have exceeded the allowed API rate limit'


class ICRequestError(Exception):
    __doc__ = 'Base error for request failures'

    def __init__(self, msg, request_id):
        self.msg = msg
        self.request_id = request_id


class ICFailedRequest(ICRequestError):
    __doc__ = 'Raised when a provisioning request failed.'


class ICTimeoutError(ICRequestError):
    __doc__ = 'Raised when a request does not finish in the given time span.'