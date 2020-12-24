# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/unshare.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 1600 bytes
"""Wrapper for unshare(2) system call."""
import logging, os, ctypes
from ctypes import c_int
from ctypes.util import find_library
_LOG = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if getattr(_LIBC, 'unshare', None) is None:
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)
_UNSHARE_DECL = ctypes.CFUNCTYPE(c_int, c_int, use_errno=True)
_UNSHARE = _UNSHARE_DECL(('unshare', _LIBC))

def unshare(what):
    """disassociate parts of the process execution context.
    """
    retcode = _UNSHARE(what)
    if retcode != 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), what)


CLONE_VM = 256
CLONE_FS = 512
CLONE_FILES = 1024
CLONE_SIGHAND = 2048
CLONE_PTRACE = 8192
CLONE_VFORK = 16384
CLONE_PARENT = 32768
CLONE_THREAD = 65536
CLONE_NEWNS = 131072
CLONE_SYSVSEM = 262144
CLONE_SETTLS = 524288
CLONE_PARENT_SETTID = 1048576
CLONE_CHILD_CLEARTID = 2097152
CLONE_DETACHED = 4194304
CLONE_UNTRACED = 8388608
CLONE_CHILD_SETTID = 16777216
CLONE_NEWUTS = 67108864
CLONE_NEWIPC = 134217728
CLONE_NEWUSER = 268435456
CLONE_NEWPID = 536870912
CLONE_NEWNET = 1073741824
CLONE_IO = 2147483648