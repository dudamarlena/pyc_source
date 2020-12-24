# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/exceptions.py
# Compiled at: 2019-11-20 16:41:05
# Size of source mod 2**32: 379 bytes


class UninitializedError(Exception):
    __doc__ = ' Project has not been initialized '


class ResourceNotFound(Exception):
    __doc__ = ' Requested document is not found '


class AlreadyExistsError(Exception):
    __doc__ = ' Resource already exists '


class RequestFailedError(Exception):
    __doc__ = ' Request went wrong '


class ConnectionFailed(Exception):
    __doc__ = ' Could not connect to Lingotek '