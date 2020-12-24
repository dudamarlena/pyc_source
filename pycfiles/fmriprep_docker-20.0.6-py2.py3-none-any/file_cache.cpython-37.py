# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_vendor/cachecontrol/caches/file_cache.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 4153 bytes
import hashlib, os
from textwrap import dedent
from ..cache import BaseCache
from ..controller import CacheController
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = (
     IOError, OSError)

def _secure_open_write(filename, fmode):
    flags = os.O_WRONLY
    flags |= os.O_CREAT | os.O_EXCL
    if hasattr(os, 'O_NOFOLLOW'):
        flags |= os.O_NOFOLLOW
    if hasattr(os, 'O_BINARY'):
        flags |= os.O_BINARY
    try:
        os.remove(filename)
    except (IOError, OSError):
        pass

    fd = os.open(filename, flags, fmode)
    try:
        return os.fdopen(fd, 'wb')
    except:
        os.close(fd)
        raise


class FileCache(BaseCache):

    def __init__(self, directory, forever=False, filemode=384, dirmode=448, use_dir_lock=None, lock_class=None):
        if use_dir_lock is not None:
            if lock_class is not None:
                raise ValueError('Cannot use use_dir_lock and lock_class together')
        try:
            from lockfile import LockFile
            from lockfile.mkdirlockfile import MkdirLockFile
        except ImportError:
            notice = dedent('\n            NOTE: In order to use the FileCache you must have\n            lockfile installed. You can install it via pip:\n              pip install lockfile\n            ')
            raise ImportError(notice)
        else:
            if use_dir_lock:
                lock_class = MkdirLockFile
            elif lock_class is None:
                lock_class = LockFile
            self.forever = forever
            self.filemode = filemode
            self.dirmode = dirmode
            self.lock_class = lock_class

    @staticmethod
    def encode(x):
        return hashlib.sha224(x.encode()).hexdigest()

    def _fn(self, name):
        hashed = self.encode(name)
        parts = list(hashed[:5]) + [hashed]
        return (os.path.join)(self.directory, *parts)

    def get(self, key):
        name = self._fn(key)
        try:
            with open(name, 'rb') as (fh):
                return fh.read()
        except FileNotFoundError:
            return

    def set(self, key, value):
        name = self._fn(key)
        try:
            os.makedirs(os.path.dirname(name), self.dirmode)
        except (IOError, OSError):
            pass

        with self.lock_class(name) as (lock):
            with _secure_open_write(lock.path, self.filemode) as (fh):
                fh.write(value)

    def delete(self, key):
        name = self._fn(key)
        if not self.forever:
            try:
                os.remove(name)
            except FileNotFoundError:
                pass


def url_to_file_path(url, filecache):
    """Return the file cache path based on the URL.

    This does not ensure the file exists!
    """
    key = CacheController.cache_url(url)
    return filecache._fn(key)