# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/client/exceptions.py
# Compiled at: 2020-03-30 13:58:22
# Size of source mod 2**32: 356 bytes


class SentryBlockException(Exception):
    pass


class AccountTypeException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class RateLimitException(Exception):
    pass


class AccessDeniedException(Exception):
    pass


class ChallengeRequiredException(Exception):
    pass