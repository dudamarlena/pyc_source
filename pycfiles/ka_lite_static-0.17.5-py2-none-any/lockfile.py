# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/lib/lockfile.py
# Compiled at: 2018-07-11 18:15:31
"""
Platform-independent file locking. Inspired by and modeled after zc.lockfile.
"""
import os
try:
    import msvcrt
except ImportError:
    pass

try:
    import fcntl
except ImportError:
    pass

class LockError(Exception):
    """Could not obtain a lock"""
    msg = 'Unable to lock %r'

    def __init__(self, path):
        super(LockError, self).__init__(self.msg % path)


class UnlockError(LockError):
    """Could not release a lock"""
    msg = 'Unable to unlock %r'


class LockFile(object):
    """
    A default, naive locking implementation. Always fails if the file
    already exists.
    """

    def __init__(self, path):
        self.path = path
        try:
            fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_EXCL)
        except OSError:
            raise LockError(self.path)

        os.close(fd)

    def release(self):
        os.remove(self.path)

    def remove(self):
        pass


class SystemLockFile(object):
    """
    An abstract base class for platform-specific locking.
    """

    def __init__(self, path):
        self.path = path
        try:
            self.fp = open(path, 'r+')
        except IOError:
            self.fp = open(path, 'a+')

        try:
            self._lock_file()
        except:
            self.fp.seek(1)
            self.fp.close()
            del self.fp
            raise

        self.fp.write(' %s\n' % os.getpid())
        self.fp.truncate()
        self.fp.flush()

    def release(self):
        if not hasattr(self, 'fp'):
            return
        self._unlock_file()
        self.fp.close()
        del self.fp

    def remove(self):
        """
        Attempt to remove the file
        """
        try:
            os.remove(self.path)
        except:
            pass

    def _unlock_file(self):
        """Attempt to obtain the lock on self.fp. Raise UnlockError if not
        released."""
        pass


class WindowsLockFile(SystemLockFile):

    def _lock_file(self):
        try:
            msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
        except IOError:
            raise LockError(self.fp.name)

    def _unlock_file(self):
        try:
            self.fp.seek(0)
            msvcrt.locking(self.fp.fileno(), msvcrt.LK_UNLCK, 1)
        except IOError:
            raise UnlockError(self.fp.name)


if 'msvcrt' in globals():
    LockFile = WindowsLockFile

class UnixLockFile(SystemLockFile):

    def _lock_file(self):
        flags = fcntl.LOCK_EX | fcntl.LOCK_NB
        try:
            fcntl.flock(self.fp.fileno(), flags)
        except IOError:
            raise LockError(self.fp.name)


if 'fcntl' in globals():
    LockFile = UnixLockFile