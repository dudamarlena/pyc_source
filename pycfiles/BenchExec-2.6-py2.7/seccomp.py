# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/seccomp.py
# Compiled at: 2020-05-07 05:52:35
"""Utility functions adding a seccomp filter."""
from __future__ import absolute_import, division, print_function, unicode_literals
import ctypes
from ctypes import c_int, c_uint, c_uint32, c_char_p, c_void_p
import errno, logging, os, threading, benchexec.libc as libc
SCMP_ACT_ALLOW = 2147418112
SCMP_ACT_ENOSYS = 327680 | errno.ENOSYS
_scmp_filter_ctx = c_void_p
_SECCOMP_MODE_FILTER = 2
_ALLOWED_COMPATIBILITY_ARCHITECTURES = [
 b'x86', b'x32', b'arm']
_AVAILABLE = None
_LOAD_LOCK = threading.Lock()
_lib = None
_check_errno = libc._check_errno

def _check_null(result, func, arguments):
    """Check that a ctypes function returned something else than null."""
    if result:
        return result
    func_name = getattr(func, b'__name__', b'__unknown__')
    raise OSError(func_name + b'(' + (b', ').join(map(str, arguments)) + b') returned null')


def _load_seccomp():
    global _lib
    try:
        libc.prctl(libc.PR_GET_SECCOMP, 0, 0, 0, 0)
    except OSError as e:
        logging.warning(b'Seccomp is not available, container isolation is degraded (%s).', os.strerror(e.errno))
        return False

    try:
        libc.prctl(libc.PR_SET_SECCOMP, _SECCOMP_MODE_FILTER, 0, 0, 0)
    except OSError as e:
        if e.errno != errno.EFAULT:
            logging.warning(b'Unexpected failure when enabling seccomp filter, container isolation is degraded (%s).', e)
            return False
    else:
        logging.warning(b'Unexpected failure when enabling seccomp filter, container isolation is degraded.')
        return False

    try:
        _lib = ctypes.CDLL(b'libseccomp.so.2', use_errno=True)
    except OSError as e:
        logging.warning(b'Could not load libseccomp2, please install it for improved container isolation (%s).', e)
        return False

    _lib.seccomp_init.argtypes = [c_uint32]
    _lib.seccomp_init.restype = _scmp_filter_ctx
    _lib.seccomp_init.errcheck = _check_null
    _lib.seccomp_release.argtypes = [
     _scmp_filter_ctx]
    _lib.seccomp_release.restype = None
    _lib.seccomp_export_pfc.argtypes = [
     _scmp_filter_ctx, c_int]
    _lib.seccomp_export_pfc.errcheck = _check_errno
    _lib.seccomp_load.argtypes = [
     _scmp_filter_ctx]
    _lib.seccomp_load.errcheck = _check_errno
    _lib.seccomp_arch_resolve_name.argtypes = [
     c_char_p]
    _lib.seccomp_arch_resolve_name.restype = c_uint32
    _lib.seccomp_arch_add.argtypes = [
     _scmp_filter_ctx, c_uint32]
    _lib.seccomp_arch_add.errcheck = _check_errno
    _lib.seccomp_syscall_resolve_name.argtypes = [
     c_char_p]
    _lib.seccomp_syscall_resolve_name.restype = c_int
    _lib.seccomp_rule_add.argtypes = [
     _scmp_filter_ctx, c_uint32, c_int, c_uint]
    _lib.seccomp_rule_add.errcheck = _check_errno
    return True


def is_available():
    """
    Check if seccomp is available and expected to work on this system.
    If seccomp is not available an appropriate warning is logged.
    """
    global _AVAILABLE
    with _LOAD_LOCK:
        if _AVAILABLE is None:
            _AVAILABLE = _load_seccomp()
        return _AVAILABLE
    return


class SeccompFilter(object):
    """
    Encapsulates a seccomp filter that can be incrementally built and loaded.
    This class is a single-use context manager,
    it is recommended to use it in a with statement.
    This class can only be used if is_available() returns True.
    """

    def __init__(self, default_action=SCMP_ACT_ALLOW):
        """
        Create instance and specify default action for all syscalls
        that are not matched by any rule.
        """
        assert is_available()
        self.filter = _lib.seccomp_init(default_action)
        for arch in _ALLOWED_COMPATIBILITY_ARCHITECTURES:
            _lib.seccomp_arch_add(self.filter, _lib.seccomp_arch_resolve_name(arch))

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.free()

    def add_rule(self, action, syscall):
        """
        Add a rule for a specific syscall.
        @param action: A number like SCMP_ACT_ALLOW or SCMP_ACT_ENOSYS
        @param syscall: A syscall name or number (on the native architecture)
        """
        if not isinstance(syscall, int):
            syscall = _lib.seccomp_syscall_resolve_name(syscall)
        _lib.seccomp_rule_add(self.filter, action, syscall, 0)

    def activate(self):
        """Activate the given seccomp filter for the current process in the kernel."""
        _lib.seccomp_load(self.filter)

    def print_to(self, fd):
        """Print debug info about the current filter to the given file descriptor."""
        _lib.seccomp_export_pfc(self.filter, fd)

    def free(self):
        _lib.seccomp_release(self.filter)
        self.filter = None
        return