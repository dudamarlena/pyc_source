# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aio_dprcon/exceptions.py
# Compiled at: 2017-11-16 18:28:43
# Size of source mod 2**32: 268 bytes


class RconException(Exception):
    pass


class RconCommandFailed(RconException):
    pass


class RconCommandTimeout(RconCommandFailed):
    pass


class RconCommandRetryNumberExceeded(RconCommandFailed):
    pass


class InvalidConfigException(Exception):
    pass