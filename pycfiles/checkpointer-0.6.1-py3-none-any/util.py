# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/util.py
# Compiled at: 2009-01-08 17:03:56
__doc__ = 'Utility methods and constants'
from __future__ import with_statement
import os, fcntl, pickle, hashlib
from fnmatch import fnmatch
__all__ = [
 'sha1_hash', 'matches_any_pattern', 'filter_all_patterns',
 'ascending_length', 'descending_length', 'filter_duplicates',
 'PickleProperty', 'acquire_lock', 'release_lock']

def ascending_length(x, y):
    return len(x) - len(y)


def descending_length(x, y):
    return len(y) - len(x)


def filter_all_patterns(paths, patterns):
    """Return only those paths that match no patterns"""
    return [ p for p in paths if not matches_any_pattern(p, patterns) ]


def matches_any_pattern(path, patterns):
    """Test if path matches any of the supplied patterns (ex: '*.jpg')"""
    return any((fnmatch(path, pattern) for pattern in patterns))


def filter_duplicates(sequence):
    """Return sequence with duplicates removed.  Preserves order."""
    seen = set()
    return [ x for x in sequence if x not in seen if not seen.add(x) ]


def sha1_hash(path):
    """Return a sha1 hash of path.
    
    For regular files, a sha1 hash of the data is returned.
    For directories, a sha1 hash of the directory name is returned.
    For links, a sha1 hash of the target path name is returned.
    For unsupported file types, None is returned.
    
    """
    h = hashlib.sha1()
    if os.path.islink(path):
        target = os.path.realpath(path)
        h.update(target)
    elif os.path.isdir(path):
        h.update(path)
    elif os.path.isfile(path):
        with open(path, 'rb') as (f):
            hash_buffer_size = 1024
            while True:
                data = f.read(hash_buffer_size)
                if data:
                    h.update(data)
                else:
                    break

    else:
        return
    return h.hexdigest()


class PickleProperty(object):
    """Descriptor that gets/sets file data"""

    def __init__(self, path_getter):
        self.path_getter = path_getter

    def __get__(self, instance, owner):
        """Return the data from the file."""
        path = self.path_getter(instance)
        try:
            with open(path, 'rb') as (f):
                return pickle.load(f)
        except (OSError, IOError), e:
            raise AttributeError('Could not read file %r: %s' % (path, e))

    def __set__(self, instance, value):
        """Create the data file if necesary, and store data into it."""
        path = self.path_getter(instance)
        try:
            with open(path, 'wb') as (f):
                pickle.dump(value, f, -1)
        except (OSError, IOError), e:
            raise AttributeError('Could not create file %r: %s' % (path, e))


def acquire_lock(lockfile_path, LockedException):
    """Acquire and return a lock using the given lockfile as the semaphore."""
    try:
        f = open(lockfile_path, 'a')
    except (OSError, IOError), e:
        raise FileError('Could not create/open lockfile %r: %s' % (
         lockfile_path, e))

    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError, e:
        raise LockedException()

    try:
        f_readonly = open(lockfile_path, 'r')
        stale_pid = f_readonly.readline()
    except (OSError, IOError), e:
        raise FileError('Could not read from lockfile %r: %s' % (
         lockfile_path, e))

    if not stale_pid:
        f.write(str(os.getpid()))
        f.flush()
        if hasattr(fcntl, 'F_FULLFSYNC'):
            fcntl.fcntl(f, fcntl.F_FULLFSYNC)
    else:
        raise LockedException()

    class Lock(object):
        pass

    lock = Lock()
    lock.lockfile = f
    lock.lockfile_readonly = f_readonly
    lock.lockfile_path = lockfile_path
    return lock


def release_lock(lock):
    """Release the lock."""
    try:
        fcntl.lockf(lock.lockfile, fcntl.LOCK_UN)
        lock.lockfile.close()
        lock.lockfile_readonly.close()
        os.remove(lock.lockfile_path)
    except (OSError, IOError), e:
        raise FileError('Could not remove lockfile %r: %s' % (
         lock.lockfile_path, e))