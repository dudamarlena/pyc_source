# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faisal/Developer/Projects/github/flickrsmartsync/flickrapi/tokencache.py
# Compiled at: 2014-06-18 08:36:36
"""Persistent token cache management for the Flickr API"""
import os.path, logging, time
from flickrapi.exceptions import LockingError
logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
__all__ = ('TokenCache', 'SimpleTokenCache')

class SimpleTokenCache(object):
    """In-memory token cache."""

    def __init__(self):
        self.token = None
        return

    def forget(self):
        """Removes the cached token"""
        self.token = None
        return


class TokenCache(object):
    """On-disk persistent token cache for a single application.

    The application is identified by the API key used. Per
    application multiple users are supported, with a single
    token per user.
    """

    def __init__(self, api_key, username=None):
        """Creates a new token cache instance"""
        self.api_key = api_key
        self.username = username
        self.memory = {}
        self.path = os.path.join('~', '.flickr')

    def get_cached_token_path(self):
        """Return the directory holding the app data."""
        return os.path.expanduser(os.path.join(self.path, self.api_key))

    def get_cached_token_filename(self):
        """Return the full pathname of the cached token file."""
        if self.username:
            filename = 'auth-%s.token' % self.username
        else:
            filename = 'auth.token'
        return os.path.join(self.get_cached_token_path(), filename)

    def get_cached_token(self):
        """Read and return a cached token, or None if not found.

        The token is read from the cached token file.
        """
        if self.username in self.memory:
            return self.memory[self.username]
        else:
            try:
                f = open(self.get_cached_token_filename(), 'r')
                token = f.read()
                f.close()
                return token.strip()
            except IOError:
                return

            return

    def set_cached_token(self, token):
        """Cache a token for later use."""
        self.memory[self.username] = token
        path = self.get_cached_token_path()
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(self.get_cached_token_filename(), 'w')
        f.write(token)
        f.close()

    def forget(self):
        """Removes the cached token"""
        if self.username in self.memory:
            del self.memory[self.username]
        filename = self.get_cached_token_filename()
        if os.path.exists(filename):
            os.unlink(filename)

    token = property(get_cached_token, set_cached_token, forget, 'The cached token')


class LockingTokenCache(TokenCache):
    """Locks the token cache when reading or updating it, so that
    multiple processes can safely use the same API key.
    """

    def get_lock_name(self):
        """Returns the filename of the lock."""
        token_name = self.get_cached_token_filename()
        return '%s-lock' % token_name

    lock = property(get_lock_name)

    def get_pidfile_name(self):
        """Returns the name of the pidfile in the lock directory."""
        return os.path.join(self.lock, 'pid')

    pidfile_name = property(get_pidfile_name)

    def get_lock_pid(self):
        """Returns the PID that is stored in the lock directory, or
        None if there is no such file.
        """
        filename = self.pidfile_name
        if not os.path.exists(filename):
            return
        else:
            pidfile = open(filename)
            try:
                pid = pidfile.read()
                if pid:
                    return int(pid)
            finally:
                pidfile.close()

            return

    def acquire(self, timeout=60):
        """Locks the token cache for this key and username.

        If the token cache is already locked, waits until it is
        released. Throws an exception when the lock cannot be acquired
        after ``timeout`` seconds.
        """
        lockpid = self.get_lock_pid()
        if lockpid == os.getpid():
            LOG.debug('The lock is ours, continuing')
            return
        lock = self.get_lock_name()
        LOG.debug('Acquiring lock %s' % lock)
        start_time = time.time()
        while True:
            try:
                os.makedirs(lock)
                break
            except OSError:
                if not os.path.exists(lock):
                    LOG.error('Unable to acquire lock %s, aborting' % lock)
                    raise
                if time.time() - start_time >= timeout:
                    raise LockingError('Unable to acquire lock ' + '%s, aborting' % lock)
                LOG.debug('Unable to acquire lock, waiting')
                time.sleep(0.1)

        LOG.debug('Lock acquired, writing our PID')
        pidfile = open(self.pidfile_name, 'w')
        try:
            pidfile.write('%s' % os.getpid())
        finally:
            pidfile.close()

    def release(self):
        """Unlocks the token cache for this key."""
        lock = self.get_lock_name()
        if not os.path.exists(lock):
            LOG.warn('Trying to release non-existing lock %s' % lock)
            return
        lockpid = self.get_lock_pid()
        if lockpid and lockpid != os.getpid():
            raise LockingError(('Lock %s is NOT ours, but belongs ' + 'to PID %i, unable to release.') % (lock,
             lockpid))
        LOG.debug('Releasing lock %s' % lock)
        pidfile = self.pidfile_name
        if os.path.exists(pidfile):
            os.remove(pidfile)
        os.removedirs(lock)

    def __del__(self):
        """Cleans up any existing lock."""
        lock = self.get_lock_name()
        if not os.path.exists(lock):
            return
        lockpid = self.get_lock_pid()
        if lockpid and lockpid != os.getpid():
            return
        self.release()

    def locked(method):
        """Decorator, ensures the method runs in a locked cache."""

        def locker(self, *args, **kwargs):
            self.acquire()
            try:
                return method(self, *args, **kwargs)
            finally:
                self.release()

        return locker

    @locked
    def get_cached_token(self):
        """Read and return a cached token, or None if not found.

        The token is read from the cached token file.
        """
        return TokenCache.get_cached_token(self)

    @locked
    def set_cached_token(self, token):
        """Cache a token for later use."""
        TokenCache.set_cached_token(self, token)

    @locked
    def forget(self):
        """Removes the cached token"""
        TokenCache.forget(self)

    token = property(get_cached_token, set_cached_token, forget, 'The cached token')