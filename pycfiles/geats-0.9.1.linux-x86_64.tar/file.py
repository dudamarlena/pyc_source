# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/lock/file.py
# Compiled at: 2012-06-03 06:49:57
import os.path, hashlib, fcntl
from abstract import AbstractLock
import warnings, time

class FileLock(AbstractLock):
    """
    A simple file-based lock.  It uses an fcntl-lock to control
    access to the lock directory.
    """

    def init(self):
        lock_dir = self.config.get('lock_directory', '/var/lock/geats')
        if not os.path.exists(lock_dir):
            os.mkdir(lock_dir)
        self.dirlockfile = os.path.join(lock_dir, 'LOCK')
        filename = hashlib.md5(self.key).hexdigest() + '.lock'
        self.lockfile = os.path.join(lock_dir, filename)
        self.locked = None
        return

    def acquire(self):
        lockfd = open(self.dirlockfile, 'w')
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX)
        except IOError:
            lockfd.close()
            return False

        try:
            if os.path.exists(self.lockfile):
                return False
            else:
                fd = open(self.lockfile, 'w')
                fd.write('%s\n' % (self.key,))
                fd.close()
                self.locked = True
                return True

        finally:
            fcntl.flock(lockfd, fcntl.LOCK_UN)
            lockfd.close()

        return False

    def release(self):
        lockfd = open(self.dirlockfile, 'w')
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX)
        except IOError:
            lockfd.close()
            return False

        try:
            if os.path.exists(self.lockfile):
                os.unlink(self.lockfile)
            self.locked = False
        finally:
            fcntl.flock(lockfd, fcntl.LOCK_UN)
            lockfd.close()

    def __del__(self):
        if self.locked:
            warnings.warn('Unreleased lock: %s' % self.key)
            self.release()