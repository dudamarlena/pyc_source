# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/signalfd.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 5787 bytes
"""Wrapper for signalfd(2) system call."""
import errno, logging, os, ctypes
from ctypes import c_int, c_void_p, c_uint32, c_uint64, c_uint8, c_int32
from ctypes.util import find_library
import enum
from ._sigsetops import SigSet, sigaddset, sigfillset
_LOGGER = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if getattr(_LIBC, 'signalfd', None) is None:
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)
_SIGNALFD_DECL = ctypes.CFUNCTYPE(c_int, c_int, c_void_p, c_int, use_errno=True)
_SIGNALFD = _SIGNALFD_DECL(('signalfd', _LIBC))

def signalfd(sigset, flags=0, prev_fd=-1):
    """create/update a signal file descriptor.
    """
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

    new_set_p = ctypes.pointer(new_set)
    fileno = _SIGNALFD(prev_fd, new_set_p, flags)
    if fileno < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err), 'signalfd(%r, %r, %r)' % (prev_fd, new_set, flags))
    return fileno


class SFDFlags(enum.IntEnum):
    __doc__ = 'Flags supported by SignalFD.'
    NONBLOCK = 2048
    CLOEXEC = 524288


SFD_NONBLOCK = SFDFlags.NONBLOCK
SFD_CLOEXEC = SFDFlags.CLOEXEC

class SFDSigInfo(ctypes.Structure):
    __doc__ = 'The signalfd_siginfo structure.\n\n    The format of the signalfd_siginfo structure(s) returned by read(2)s from a\n    signalfd file descriptor is as follows:\n\n        struct signalfd_siginfo {\n            uint32_t ssi_signo;   /* Signal number */\n            int32_t  ssi_errno;   /* Error number (unused) */\n            int32_t  ssi_code;    /* Signal code */\n            uint32_t ssi_pid;     /* PID of sender */\n            uint32_t ssi_uid;     /* Real UID of sender */\n            int32_t  ssi_fd;      /* File descriptor (SIGIO) */\n            uint32_t ssi_tid;     /* Kernel timer ID (POSIX timers)\n            uint32_t ssi_band;    /* Band event (SIGIO) */\n            uint32_t ssi_overrun; /* POSIX timer overrun count */\n            uint32_t ssi_trapno;  /* Trap number that caused signal */\n            int32_t  ssi_status;  /* Exit status or signal (SIGCHLD) */\n            int32_t  ssi_int;     /* Integer sent by sigqueue(2) */\n            uint64_t ssi_ptr;     /* Pointer sent by sigqueue(2) */\n            uint64_t ssi_utime;   /* User CPU time consumed (SIGCHLD) */\n            uint64_t ssi_stime;   /* System CPU time consumed (SIGCHLD) */\n            uint64_t ssi_addr;    /* Address that generated signal\n                                     (for hardware-generated signals) */\n            uint8_t  pad[X];      /* Pad size to 128 bytes (allow for\n                                      additional fields in the future) */\n        };\n\n    '
    _FIELDS = [
     (
      'ssi_signo', c_uint32),
     (
      'ssi_errno', c_int32),
     (
      'ssi_code', c_int32),
     (
      'ssi_pid', c_uint32),
     (
      'ssi_uid', c_uint32),
     (
      'ssi_fd', c_int32),
     (
      'ssi_tid', c_uint32),
     (
      'ssi_band', c_uint32),
     (
      'ssi_overrun', c_uint32),
     (
      'ssi_trapno', c_uint32),
     (
      'ssi_status', c_int32),
     (
      'ssi_int', c_int32),
     (
      'ssi_ptr', c_uint64),
     (
      'ssi_utime', c_uint64),
     (
      'ssi_stime', c_uint64),
     (
      'ssi_addr', c_uint64)]
    _SFDSigInfo__PADWORDS = 128 - sum([ctypes.sizeof(field[1]) for field in _FIELDS])
    _fields_ = _FIELDS + [
     (
      '_pad', c_uint8 * _SFDSigInfo__PADWORDS)]


def signalfd_read(sfd):
    """Read signalfd_siginfo data from a signalfd filedescriptor.
    """
    try:
        data = os.read(sfd, ctypes.sizeof(SFDSigInfo))
    except OSError as err:
        if err.errno != errno.EINTR:
            raise
        return

    return SFDSigInfo.from_buffer_copy(data)


__all__ = [
 'SFD_NONBLOCK',
 'SFD_CLOEXEC',
 'signalfd',
 'signalfd_read']