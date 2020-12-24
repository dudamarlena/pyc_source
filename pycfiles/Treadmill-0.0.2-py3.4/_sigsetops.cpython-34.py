# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/_sigsetops.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 3424 bytes
"""Wrapper for sigsetops(3)."""
import logging, os, ctypes
from ctypes import c_int, c_ulong, c_void_p
from ctypes.util import find_library
_LOGGER = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if any([getattr(_LIBC, op, None) is None for op in ['sigemptyset', 'sigfillset', 'sigaddset', 'sigdelset']]):
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)

class SigSet(ctypes.Structure):
    __doc__ = 'type sigset_t;\n    '
    _SIGSET_NWORDS = 1024 / (8 * ctypes.sizeof(ctypes.c_ulong))
    _fields_ = [
     (
      'sigset', c_ulong * _SIGSET_NWORDS)]


_SIGEMPTYSET_DECL = ctypes.CFUNCTYPE(c_int, c_void_p, use_errno=True)
_SIGEMPTYSET = _SIGEMPTYSET_DECL(('sigemptyset', _LIBC))

def sigemptyset(sigset):
    """int sigemptyset(sigset_t *set).
    """
    sigset_p = ctypes.pointer(sigset)
    res = _SIGEMPTYSET(sigset_p)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), 'sigemptyset(%r)' % sigset)
    return res


_SIGFILLSET_DECL = ctypes.CFUNCTYPE(c_int, c_void_p, use_errno=True)
_SIGFILLSET = _SIGFILLSET_DECL(('sigfillset', _LIBC))

def sigfillset(sigset):
    """int sigfillset(sigset_t *set).
    """
    sigset_p = ctypes.pointer(sigset)
    res = _SIGFILLSET(sigset_p)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), 'sigfillset(%r)' % sigset)
    return res


_SIGADDSET_DECL = ctypes.CFUNCTYPE(c_int, c_void_p, use_errno=True)
_SIGADDSET = _SIGADDSET_DECL(('sigaddset', _LIBC))

def sigaddset(sigset, signum):
    """int sigaddset(sigset_t *set, int signum).
    """
    sigset_p = ctypes.pointer(sigset)
    res = _SIGADDSET(sigset_p, signum)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), 'sigaddset(%r, %r)' % (sigset, signum))
    return res


_SIGDELSET_DECL = ctypes.CFUNCTYPE(c_int, c_void_p, use_errno=True)
_SIGDELSET = _SIGDELSET_DECL(('sigdelset', _LIBC))

def sigdelset(sigset, signum):
    """int sigdelset(sigset_t *set, int signum).
    """
    sigset_p = ctypes.pointer(sigset)
    res = _SIGDELSET(sigset_p, signum)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), 'sigdelset(%r, %r)' % (sigset, signum))
    return res


__all__ = [
 'SigSet',
 'sigaddset',
 'sigdelset',
 'sigemptyset',
 'sigfillset']