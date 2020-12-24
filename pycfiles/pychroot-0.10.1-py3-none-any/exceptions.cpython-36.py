# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/pkgcore/pychroot/build/lib/pychroot/exceptions.py
# Compiled at: 2019-12-01 01:06:22
# Size of source mod 2**32: 697 bytes
"""Various chroot-related exception classes"""
import os

class ChrootError(Exception):
    __doc__ = 'Exception raised when there is an error setting up a chroot.'

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
    __doc__ = 'Exception raised when there is an error setting up chroot bind mounts.'