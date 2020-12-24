# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/sockspy/core/exceptions.py
# Compiled at: 2017-07-28 03:12:25
# Size of source mod 2**32: 285 bytes


class ReadOrWriteNoDataError(Exception):
    __doc__ = '\n    This exception is thrown when a socket reads or writes 0 byte, which indicates that the remote side is disconnected.\n    '


class StatusRegisterError(Exception):
    pass