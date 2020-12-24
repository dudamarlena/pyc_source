# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\cache.py
# Compiled at: 2015-01-11 13:52:03
from __future__ import print_function
import time, threading, os
try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    import hashlib
except ImportError:
    import md5 as hashlib

try:
    import fcntl
except ImportError:
    pass

class Cache(object):
    """Cache interface"""

    def __init__(self, timeout=60):
        """Initialize the cache
            timeout: number of seconds to keep a cached entry
        """
        self.timeout = timeout

    def store(self, key, value):
        """Add new record to cache
            key: entry key
            value: data of entry
        """
        raise NotImplementedError

    def get(self, key, timeout=None):
        """Get cached entry if exists and not expired
            key: which entry to get
            timeout: override timeout with this value [optional]
        """
        raise NotImplementedError

    def count(self):
        """Get count of entries currently stored in cache"""
        raise NotImplementedError

    def cleanup(self):
        """Delete any expired entries in cache."""
        raise NotImplementedError

    def flush(self):
        """Delete all cached entries"""
        raise NotImplementedError


class MemoryCache(Cache):
    """In-memory cache"""

    def __init__(self, timeout=60):
        Cache.__init__(self, timeout)
        self._entries = {}
        self.lock = threading.Lock()

    def __getstate__(self):
        return {'entries': self._entries, 'timeout': self.timeout}

    def __setstate__(self, state):
        self.lock = threading.Lock()
        self._entries = state['entries']
        self.timeout = state['timeout']

    def _is_expired(self, entry, timeout):
        return timeout > 0 and time.time() - entry[0] >= timeout

    def store(self, key, value):
        self.lock.acquire()
        self._entries[key] = (time.time(), value)
        self.lock.release()

    def get(self, key, timeout=None):
        self.lock.acquire()
        try:
            entry = self._entries.get(key)
            if not entry:
                return
            if timeout is None:
                timeout = self.timeout
            if self._is_expired(entry, timeout):
                del self._entries[key]
                return
            return entry[1]
        finally:
            self.lock.release()

        return

    def count(self):
        return len(self._entries)

    def cleanup(self):
        self.lock.acquire()
        try:
            for k, v in self._entries.items():
                if self._is_expired(v, self.timeout):
                    del self._entries[k]

        finally:
            self.lock.release()

    def flush(self):
        self.lock.acquire()
        self._entries.clear()
        self.lock.release()


class FileCache(Cache):
    """File-based cache"""
    cache_locks = {}

    def __init__(self, cache_dir, timeout=60):
        Cache.__init__(self, timeout)
        if os.path.exists(cache_dir) is False:
            os.mkdir(cache_dir)
        self.cache_dir = cache_dir
        if cache_dir in FileCache.cache_locks:
            self.lock = FileCache.cache_locks[cache_dir]
        else:
            self.lock = threading.Lock()
            FileCache.cache_locks[cache_dir] = self.lock
        if os.name == 'posix':
            self._lock_file = self._lock_file_posix
            self._unlock_file = self._unlock_file_posix
        elif os.name == 'nt':
            self._lock_file = self._lock_file_win32
            self._unlock_file = self._unlock_file_win32
        else:
            print('Warning! FileCache locking not supported on this system!')
            self._lock_file = self._lock_file_dummy
            self._unlock_file = self._unlock_file_dummy

    def _get_path(self, key):
        md5 = hashlib.md5()
        md5.update(key)
        return os.path.join(self.cache_dir, md5.hexdigest())

    def _lock_file_dummy(self, path, exclusive=True):
        return

    def _unlock_file_dummy(self, lock):
        pass

    def _lock_file_posix(self, path, exclusive=True):
        lock_path = path + '.lock'
        if exclusive is True:
            f_lock = open(lock_path, 'w')
            fcntl.lockf(f_lock, fcntl.LOCK_EX)
        else:
            f_lock = open(lock_path, 'r')
            fcntl.lockf(f_lock, fcntl.LOCK_SH)
        if os.path.exists(lock_path) is False:
            f_lock.close()
            return None
        else:
            return f_lock

    def _unlock_file_posix(self, lock):
        lock.close()

    def _lock_file_win32(self, path, exclusive=True):
        return

    def _unlock_file_win32(self, lock):
        pass

    def _delete_file(self, path):
        os.remove(path)
        if os.path.exists(path + '.lock'):
            os.remove(path + '.lock')

    def store(self, key, value):
        path = self._get_path(key)
        self.lock.acquire()
        try:
            f_lock = self._lock_file(path)
            datafile = open(path, 'wb')
            pickle.dump((time.time(), value), datafile)
            datafile.close()
            self._unlock_file(f_lock)
        finally:
            self.lock.release()

    def get(self, key, timeout=None):
        return self._get(self._get_path(key), timeout)

    def _get(self, path, timeout):
        if os.path.exists(path) is False:
            return
        else:
            self.lock.acquire()
            try:
                f_lock = self._lock_file(path, False)
                datafile = open(path, 'rb')
                created_time, value = pickle.load(datafile)
                datafile.close()
                if timeout is None:
                    timeout = self.timeout
                if timeout > 0 and time.time() - created_time >= timeout:
                    value = None
                    self._delete_file(path)
                self._unlock_file(f_lock)
                return value
            finally:
                self.lock.release()

            return

    def count(self):
        c = 0
        for entry in os.listdir(self.cache_dir):
            if entry.endswith('.lock'):
                continue
            c += 1

        return c

    def cleanup(self):
        for entry in os.listdir(self.cache_dir):
            if entry.endswith('.lock'):
                continue
            self._get(os.path.join(self.cache_dir, entry), None)

        return

    def flush(self):
        for entry in os.listdir(self.cache_dir):
            if entry.endswith('.lock'):
                continue
            self._delete_file(os.path.join(self.cache_dir, entry))


class MemCacheCache(Cache):
    """Cache interface"""

    def __init__(self, client, timeout=60):
        """Initialize the cache
            client: The memcache client
            timeout: number of seconds to keep a cached entry
        """
        self.client = client
        self.timeout = timeout

    def store(self, key, value):
        """Add new record to cache
            key: entry key
            value: data of entry
        """
        self.client.set(key, value, time=self.timeout)

    def get(self, key, timeout=None):
        """Get cached entry if exists and not expired
            key: which entry to get
            timeout: override timeout with this value [optional]. DOES NOT WORK HERE
        """
        return self.client.get(key)

    def count(self):
        """Get count of entries currently stored in cache. RETURN 0"""
        raise NotImplementedError

    def cleanup(self):
        """Delete any expired entries in cache. NO-OP"""
        raise NotImplementedError

    def flush(self):
        """Delete all cached entries. NO-OP"""
        raise NotImplementedError