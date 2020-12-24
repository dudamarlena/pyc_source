# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/libc.py
# Compiled at: 2020-05-07 05:52:35
"""This module contains function declarations for several functions of libc
(based on ctypes) and constants relevant for these functions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import ctypes as _ctypes
from ctypes import c_int, c_uint32, c_long, c_ulong, c_size_t, c_char_p, c_void_p
import os as _os
_libc = _ctypes.CDLL(b'libc.so.6', use_errno=True)
_libc_with_gil = _ctypes.PyDLL(b'libc.so.6', use_errno=True)

def _check_errno(result, func, arguments):
    assert func.restype in [c_int, c_void_p]
    if func.restype == c_int and result == -1 or func.restype == c_void_p and c_void_p(result).value == c_void_p(-1).value:
        errno = _ctypes.get_errno()
        try:
            func_name = func.__name__
        except AttributeError:
            func_name = b'__unknown__'

        msg = func_name + b'(' + (b', ').join(map(str, arguments)) + b') failed: ' + _os.strerror(errno)
        raise OSError(errno, msg)
    return result


c_off_t = c_long
clone = _libc_with_gil.clone
CLONE_CALLBACK = _ctypes.CFUNCTYPE(c_int, c_void_p)
clone.argtypes = [
 CLONE_CALLBACK,
 c_void_p,
 c_int,
 c_void_p]
clone.errcheck = _check_errno
CLONE_NEWNS = 131072
CLONE_NEWUTS = 67108864
CLONE_NEWIPC = 134217728
CLONE_NEWUSER = 268435456
CLONE_NEWPID = 536870912
CLONE_NEWNET = 1073741824
unshare = _libc.unshare
unshare.argtypes = [
 c_int]
unshare.errcheck = _check_errno
sysconf = _libc.sysconf
sysconf.argtypes = [
 c_int]
sysconf.restype = c_long
SC_PAGESIZE = 30
mmap = _libc.mmap
mmap.argtypes = [
 c_void_p,
 c_size_t,
 c_int,
 c_int,
 c_int,
 c_off_t]
mmap.restype = c_void_p
mmap.errcheck = _check_errno

def mmap_anonymous(length, prot, flags=0):
    """Allocate anonymous memory with mmap. Length must be multiple of page size."""
    return mmap(None, length, prot, flags | MAP_ANONYMOUS | MAP_PRIVATE, -1, 0)


munmap = _libc.munmap
munmap.argtypes = [
 c_void_p, c_size_t]
munmap.errcheck = _check_errno
mprotect = _libc.mprotect
mprotect.argtypes = [
 c_void_p, c_size_t, c_int]
mprotect.errcheck = _check_errno
PROT_NONE = 0
MAP_GROWSDOWN = 256
MAP_STACK = 131072
from mmap import PROT_EXEC, PROT_READ, PROT_WRITE, MAP_ANONYMOUS, MAP_PRIVATE
mount = _libc.mount
mount.argtypes = [
 c_char_p,
 c_char_p,
 c_char_p,
 c_ulong,
 c_void_p]
mount.errcheck = _check_errno
MS_RDONLY = 1
MS_NOSUID = 2
MS_NODEV = 4
MS_NOEXEC = 8
MS_REMOUNT = 32
MS_BIND = 4096
MS_MOVE = 8192
MS_REC = 16384
MS_PRIVATE = 262144
MOUNT_FLAGS = {b'ro': MS_RDONLY, 
   b'nosuid': MS_NOSUID, 
   b'nodev': MS_NODEV, 
   b'noexec': MS_NOEXEC}
umount = _libc.umount
umount.argtypes = [
 c_char_p]
umount.errcheck = _check_errno
umount2 = _libc.umount2
umount2.argtypes = [
 c_char_p, c_int]
umount2.errcheck = _check_errno
MNT_DETACH = 2
pivot_root = _libc.pivot_root
pivot_root.argtypes = [
 c_char_p, c_char_p]
pivot_root.errcheck = _check_errno
_sighandler_t = _ctypes.CFUNCTYPE(None, c_int)
_libc.signal.argtypes = [c_int, _sighandler_t]
_libc.signal.restype = c_void_p
_libc.signal.errcheck = _check_errno

def signal(signal, handler):
    """Set a signal handler similar to signal.signal(), but directly via libc."""
    _libc.signal(signal, _sighandler_t(handler))


class CapHeader(_ctypes.Structure):
    """Structure for first parameter of capset()."""
    _fields_ = (
     (
      b'version', c_uint32), (b'pid', c_int))


class CapData(_ctypes.Structure):
    """Structure for second parameter of capset()."""
    _fields_ = (
     (
      b'effective', c_uint32),
     (
      b'permitted', c_uint32),
     (
      b'inheritable', c_uint32))


capset = _libc.capset
capset.errcheck = _check_errno
capset.argtypes = [_ctypes.POINTER(CapHeader), _ctypes.POINTER(CapData * 2)]
LINUX_CAPABILITY_VERSION_3 = 537396514
CAP_SYS_ADMIN = 21
prctl = _libc.prctl
prctl.errcheck = _check_errno
prctl.argtypes = [c_int, c_ulong, c_ulong, c_ulong, c_ulong]
PR_SET_DUMPABLE = 4
PR_GET_SECCOMP = 21
PR_SET_SECCOMP = 22
SUID_DUMP_DISABLE = 0
SUID_DUMP_USER = 1
_libc.sethostname.errcheck = _check_errno
_libc.sethostname.argtypes = [c_char_p, c_size_t]

def sethostname(name):
    """Set the host name of the machine."""
    name = name.encode()
    _libc.sethostname(name, len(name))