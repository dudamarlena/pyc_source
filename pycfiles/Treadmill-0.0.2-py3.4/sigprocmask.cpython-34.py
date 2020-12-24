# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/sigprocmask.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2772 bytes
"""Wrapper for sigprocmask(2) operations."""
import logging, os, ctypes
from ctypes import c_int, c_void_p
from ctypes.util import find_library
import enum
from ._sigsetops import SigSet, sigaddset, sigfillset
_LOGGER = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if getattr(_LIBC, 'sigprocmask', None) is None:
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)
_SIGPROCMASK_DECL = ctypes.CFUNCTYPE(c_int, c_int, c_void_p, c_void_p, use_errno=True)
_SIGPROCMASK = _SIGPROCMASK_DECL(('sigprocmask', _LIBC))

def sigprocmask(how, sigset, save_mask=True):
    """Examine and change blocked signals.
    """
    how = SigProcMaskHow(how)
    if isinstance(sigset, SigSet):
        new_set = sigset
    else:
        if sigset == 'all':
            new_set = SigSet()
            sigfillset(new_set)
        else:
            new_set = SigSet()
            for signum in sigset:
                sigaddset(new_set, signum)

        if save_mask:
            old_set = SigSet()
        else:
            old_set = 0
    new_set_p = ctypes.pointer(new_set)
    old_set_p = ctypes.pointer(old_set)
    res = _SIGPROCMASK(how, new_set_p, old_set_p)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), 'sigprocmask(%r, %r, %r)' % (how, new_set, old_set))
    return old_set


class SigProcMaskHow(enum.IntEnum):
    __doc__ = 'How option supported by sigprocmask.'
    SIG_BLOCK = 0
    SIG_UNBLOCK = 1
    SIG_SETMASK = 2


SIG_BLOCK = SigProcMaskHow.SIG_BLOCK
SIG_UNBLOCK = SigProcMaskHow.SIG_UNBLOCK
SIG_SETMASK = SigProcMaskHow.SIG_SETMASK
__all__ = [
 'sigprocmask',
 'SIG_BLOCK',
 'SIG_UNBLOCK',
 'SIG_SETMASK']