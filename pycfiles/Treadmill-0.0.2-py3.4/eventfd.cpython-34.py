# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/eventfd.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2266 bytes
"""Wrapper for eventfd(2) system call."""
import logging, os, ctypes
from ctypes import c_int, c_uint
from ctypes.util import find_library
import enum
_LOGGER = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if getattr(_LIBC, 'eventfd', None) is None:
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)
_EVENTFD_DECL = ctypes.CFUNCTYPE(c_int, c_uint, c_int, use_errno=True)
_EVENTFD = _EVENTFD_DECL(('eventfd', _LIBC))

def eventfd(initval, flags):
    """create a file descriptor for event notification.
    """
    if initval < 0 or initval > 18446744073709551615:
        raise ValueError('Invalid initval: %r' % initval)
    fileno = _EVENTFD(initval, flags)
    if fileno < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), 'eventfd(%r, %r)' % (initval, flags))
    return fileno


class EFDFlags(enum.IntEnum):
    __doc__ = 'Flags supported by EventFD.'
    NONBLOCK = 2048
    CLOEXEC = 524288

    @classmethod
    def parse(cls, flags):
        """Parse EventFD flags into list of flags."""
        masks = []
        remain_flags = flags
        for flag in cls:
            if flags & flag.value:
                remain_flags ^= flag.value
                masks.append(flag)
                continue

        if remain_flags:
            masks.append(remain_flags)
        return masks


EFD_NONBLOCK = EFDFlags.NONBLOCK
EFD_CLOEXEC = EFDFlags.CLOEXEC