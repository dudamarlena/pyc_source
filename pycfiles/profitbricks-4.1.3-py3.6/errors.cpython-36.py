# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/profitbricks/errors.py
# Compiled at: 2018-07-12 06:04:26
# Size of source mod 2**32: 1553 bytes


class PBError(Exception):
    __doc__ = 'Base error for this module.'

    def __init__(self, resp, content, uri=None):
        self.resp = resp
        self.content = content
        self.uri = uri


class PBNotAuthorizedError(PBError):
    __doc__ = 'The authorization information provided is not correct'


class PBNotFoundError(PBError):
    __doc__ = 'The ProfitBricks entity was not found'


class PBValidationError(PBError):
    __doc__ = 'The HTTP data provided is not valid'


class PBRateLimitExceededError(PBError):
    __doc__ = 'The number of requests sent have exceeded the allowed API rate limit'


class PBRequestError(Exception):
    __doc__ = 'Base error for request failures'

    def __init__(self, msg, request_id):
        self.msg = msg
        self.request_id = request_id


class PBFailedRequest(PBRequestError):
    __doc__ = 'Raised when a provisioning request failed.'


class PBTimeoutError(PBRequestError):
    __doc__ = 'Raised when a request does not finish in the given time span.'