# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/profitbricks/errors.py
# Compiled at: 2018-07-12 06:04:26
# Size of source mod 2**32: 1553 bytes


class PBError(Exception):
    """PBError"""

    def __init__(self, resp, content, uri=None):
        self.resp = resp
        self.content = content
        self.uri = uri


class PBNotAuthorizedError(PBError):
    """PBNotAuthorizedError"""
    pass


class PBNotFoundError(PBError):
    """PBNotFoundError"""
    pass


class PBValidationError(PBError):
    """PBValidationError"""
    pass


class PBRateLimitExceededError(PBError):
    """PBRateLimitExceededError"""
    pass


class PBRequestError(Exception):
    """PBRequestError"""

    def __init__(self, msg, request_id):
        self.msg = msg
        self.request_id = request_id


class PBFailedRequest(PBRequestError):
    """PBFailedRequest"""
    pass


class PBTimeoutError(PBRequestError):
    """PBTimeoutError"""
    pass