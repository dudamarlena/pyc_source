# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/syscall/mount.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 3710 bytes
"""Linux mount(2) API wrapper module
"""
import logging, os, ctypes
from ctypes import c_int, c_char_p, c_ulong, c_void_p
from ctypes.util import find_library
_LOG = logging.getLogger(__name__)
_LIBC_PATH = find_library('c')
_LIBC = ctypes.CDLL(_LIBC_PATH, use_errno=True)
if not getattr(_LIBC, 'mount', None) or not getattr(_LIBC, 'umount', None) or not getattr(_LIBC, 'umount2', None):
    raise ImportError('Unsupported libc version found: %s' % _LIBC_PATH)
_MOUNT_DECL = ctypes.CFUNCTYPE(c_int, c_char_p, c_char_p, c_char_p, c_ulong, c_void_p, use_errno=True)
_MOUNT = _MOUNT_DECL(('mount', _LIBC))

def mount(source, target, fs_type, mnt_flags=()):
    """Mount ``source`` on ``target`` using filesystem type ``fs_type`` and
    mount flags ``mnt_flags``.

    NOTE: Mount data argument is not supported.
    """
    res = _MOUNT(source, target, fs_type, mnt_flags, 0)
    if res < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), 'mount(%r, %r, %r, %r)' % (source, target, fs_type, mnt_flags))
    return res


_UMOUNT_DECL = ctypes.CFUNCTYPE(c_int, c_char_p, use_errno=True)
_UMOUNT = _UMOUNT_DECL(('umount', _LIBC))
_UMOUNT2_DECL = ctypes.CFUNCTYPE(c_int, c_char_p, c_int, use_errno=True)
_UMOUNT2 = _UMOUNT2_DECL(('umount2', _LIBC))

def unmount(target, flags=None):
    """Unmount ``target``."""
    res = 0
    if flags is None:
        res = _UMOUNT(target)
        if res < 0:
            errno = ctypes.get_errno()
            raise OSError(errno, os.strerror(errno), 'umount(%r)' % (target,))
    else:
        res = _UMOUNT2(target, flags)
    if res < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), 'umount2(%r, %r)' % (target, flags))
    return res


MS_RDONLY = 1
MS_NOSUID = 2
MS_NODEV = 4
MS_NOEXEC = 8
MS_SYNCHRONOUS = 16
MS_REMOUNT = 32
MS_MANDLOCK = 64
MS_DIRSYNC = 128
MS_NOATIME = 1024
MS_NODIRATIME = 2048
MS_BIND = 4096
MS_MOVE = 8192
MS_REC = 16384
MS_UNBINDABLE = 131072
MS_PRIVATE = 262144
MS_SLAVE = 524288
MS_SHARED = 1048576
MNT_FORCE = 1
MNT_DETACH = 2
MNT_EXPIRE = 4