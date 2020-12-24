# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limiter/exceptions.py
# Compiled at: 2019-12-30 13:03:26
# Size of source mod 2**32: 483 bytes


class CapacityExhaustedException(Exception):
    __doc__ = ' Raised when a token is requested but none are available. '


class ReservationNotFoundException(Exception):
    __doc__ = ' Raised when the query result for a non-fungible token reservation is empty. '


class ThrottlingException(Exception):
    __doc__ = ' Raised when the limiter is throttled by AWS. '


class RateLimiterException(Exception):
    __doc__ = ' Raised by a limiter on unrecoverable errors when fetching a token or account limits. '