# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/pkgcore/pychroot/build/lib/pychroot/exceptions.py
# Compiled at: 2019-12-01 01:06:22
# Size of source mod 2**32: 697 bytes
__doc__ = 'Various chroot-related exception classes'
import os

class ChrootError(Exception):
    """ChrootError"""

    def __init__(self, message, errno=None):
        self.message = message
        self.args = (message,)
        if errno is not None:
            self.errno = errno
            self.strerror = os.strerror(errno)

    def __str__(self):
        error_messages = [self.message]
        if getattr(self, 'strerror', False):
            error_messages.append(self.strerror)
        return ': '.join(error_messages)


class ChrootMountError(ChrootError):
    """ChrootMountError"""
    pass