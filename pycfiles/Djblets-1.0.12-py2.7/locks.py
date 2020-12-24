# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/compat/django/core/files/locks.py
# Compiled at: 2019-06-12 01:17:17
"""
Portable file locking utilities.

Based partially on an example by Jonathan Feignberg in the Python
Cookbook [1] (licensed under the Python Software License) and a ctypes port by
Anatoly Techtonik for Roundup [2] (license [3]).

[1] http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65203
[2] http://sourceforge.net/p/roundup/code/ci/default/tree/roundup/backends/portalocker.py
[3] http://sourceforge.net/p/roundup/code/ci/default/tree/COPYING.txt
"""
import os
__all__ = ('LOCK_EX', 'LOCK_SH', 'LOCK_NB', 'lock', 'unlock')

def _fd(f):
    """Get a filedescriptor from something which could be a file or an fd."""
    if hasattr(f, 'fileno'):
        return f.fileno()
    return f


if os.name == 'nt':
    import msvcrt
    from ctypes import sizeof, c_ulong, c_void_p, c_int64, Structure, Union, POINTER, windll, byref
    from ctypes.wintypes import BOOL, DWORD, HANDLE
    LOCK_SH = 0
    LOCK_NB = 1
    LOCK_EX = 2
    if sizeof(c_ulong) != sizeof(c_void_p):
        ULONG_PTR = c_int64
    else:
        ULONG_PTR = c_ulong
    PVOID = c_void_p

    class _OFFSET(Structure):
        _fields_ = [
         (
          'Offset', DWORD),
         (
          'OffsetHigh', DWORD)]


    class _OFFSET_UNION(Union):
        _anonymous_ = [
         '_offset']
        _fields_ = [
         (
          '_offset', _OFFSET),
         (
          'Pointer', PVOID)]


    class OVERLAPPED(Structure):
        _anonymous_ = [
         '_offset_union']
        _fields_ = [
         (
          'Internal', ULONG_PTR),
         (
          'InternalHigh', ULONG_PTR),
         (
          '_offset_union', _OFFSET_UNION),
         (
          'hEvent', HANDLE)]


    LPOVERLAPPED = POINTER(OVERLAPPED)
    LockFileEx = windll.kernel32.LockFileEx
    LockFileEx.restype = BOOL
    LockFileEx.argtypes = [HANDLE, DWORD, DWORD, DWORD, DWORD, LPOVERLAPPED]
    UnlockFileEx = windll.kernel32.UnlockFileEx
    UnlockFileEx.restype = BOOL
    UnlockFileEx.argtypes = [HANDLE, DWORD, DWORD, DWORD, LPOVERLAPPED]

    def lock(f, flags):
        hfile = msvcrt.get_osfhandle(_fd(f))
        overlapped = OVERLAPPED()
        ret = LockFileEx(hfile, flags, 0, 0, 4294901760, byref(overlapped))
        return bool(ret)


    def unlock(f):
        hfile = msvcrt.get_osfhandle(_fd(f))
        overlapped = OVERLAPPED()
        ret = UnlockFileEx(hfile, 0, 0, 4294901760, byref(overlapped))
        return bool(ret)


else:
    try:
        import fcntl
        LOCK_SH = fcntl.LOCK_SH
        LOCK_NB = fcntl.LOCK_NB
        LOCK_EX = fcntl.LOCK_EX
    except (ImportError, AttributeError):
        LOCK_EX = LOCK_SH = LOCK_NB = 0

        def lock(f, flags):
            return False


        def unlock(f):
            return True


    else:

        def lock(f, flags):
            ret = fcntl.flock(_fd(f), flags)
            return ret == 0


        def unlock(f):
            ret = fcntl.flock(_fd(f), fcntl.LOCK_UN)
            return ret == 0