# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/files/locks.py
# Compiled at: 2018-07-11 18:15:30
"""
Portable file locking utilities.

Based partially on example by Jonathan Feignberg <jdf@pobox.com> in the Python
Cookbook, licensed under the Python Software License.

    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65203

Example Usage::

    >>> from django.core.files import locks
    >>> with open('./file', 'wb') as f:
    ...     locks.lock(f, locks.LOCK_EX)
    ...     f.write('Django')
"""
__all__ = ('LOCK_EX', 'LOCK_SH', 'LOCK_NB', 'lock', 'unlock')
system_type = None
try:
    import win32con, win32file, pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()
    system_type = 'nt'
except (ImportError, AttributeError):
    pass

try:
    import fcntl
    LOCK_EX = fcntl.LOCK_EX
    LOCK_SH = fcntl.LOCK_SH
    LOCK_NB = fcntl.LOCK_NB
    system_type = 'posix'
except (ImportError, AttributeError):
    pass

def fd(f):
    """Get a filedescriptor from something which could be a file or an fd."""
    return hasattr(f, 'fileno') and f.fileno() or f


if system_type == 'nt':

    def lock(file, flags):
        hfile = win32file._get_osfhandle(fd(file))
        win32file.LockFileEx(hfile, flags, 0, -65536, __overlapped)


    def unlock(file):
        hfile = win32file._get_osfhandle(fd(file))
        win32file.UnlockFileEx(hfile, 0, -65536, __overlapped)


elif system_type == 'posix':

    def lock(file, flags):
        fcntl.lockf(fd(file), flags)


    def unlock(file):
        fcntl.lockf(fd(file), fcntl.LOCK_UN)


else:
    LOCK_EX = LOCK_SH = LOCK_NB = None

    def lock(file, flags):
        pass


    def unlock(file):
        pass