# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/lockutils.py
# Compiled at: 2016-06-13 14:11:03
import errno, functools, os, shutil, tempfile, time, weakref
from eventlet import semaphore
from oslo.config import cfg
from vsm.openstack.common import fileutils
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import local
from vsm.openstack.common import log as logging
LOG = logging.getLogger(__name__)
util_opts = [
 cfg.BoolOpt('disable_process_locking', default=False, help='Whether to disable inter-process locks'),
 cfg.StrOpt('lock_path', help='Directory to use for lock files. Default to a temp directory')]
CONF = cfg.CONF
CONF.register_opts(util_opts)

class _InterProcessLock(object):
    """Lock implementation which allows multiple locks, working around
    issues like bugs.debian.org/cgi-bin/bugreport.cgi?bug=632857 and does
    not require any cleanup. Since the lock is always held on a file
    descriptor rather than outside of the process, the lock gets dropped
    automatically if the process crashes, even if __exit__ is not executed.

    There are no guarantees regarding usage by multiple green threads in a
    single process here. This lock works only between processes. Exclusive
    access between local threads should be achieved using the semaphores
    in the @synchronized decorator.

    Note these locks are released when the descriptor is closed, so it's not
    safe to close the file descriptor while another green thread holds the
    lock. Just opening and closing the lock file can break synchronisation,
    so lock files must be accessed only using this abstraction.
    """

    def __init__(self, name):
        self.lockfile = None
        self.fname = name
        return

    def __enter__(self):
        self.lockfile = open(self.fname, 'w')
        while True:
            try:
                self.trylock()
                return self
            except IOError as e:
                if e.errno in (errno.EACCES, errno.EAGAIN):
                    time.sleep(0.01)
                else:
                    raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.unlock()
            self.lockfile.close()
        except IOError:
            LOG.exception(_('Could not release the acquired lock `%s`'), self.fname)

    def trylock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()


class _WindowsLock(_InterProcessLock):

    def trylock(self):
        msvcrt.locking(self.lockfile.fileno(), msvcrt.LK_NBLCK, 1)

    def unlock(self):
        msvcrt.locking(self.lockfile.fileno(), msvcrt.LK_UNLCK, 1)


class _PosixLock(_InterProcessLock):

    def trylock(self):
        fcntl.lockf(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def unlock(self):
        fcntl.lockf(self.lockfile, fcntl.LOCK_UN)


if os.name == 'nt':
    import msvcrt
    InterProcessLock = _WindowsLock
else:
    import fcntl
    InterProcessLock = _PosixLock
_semaphores = weakref.WeakValueDictionary()

def synchronized(name, lock_file_prefix, external=False, lock_path=None):
    """Synchronization decorator.

    Decorating a method like so::

        @synchronized('mylock')
        def foo(self, *args):
           ...

    ensures that only one thread will execute the foo method at a time.

    Different methods can share the same lock::

        @synchronized('mylock')
        def foo(self, *args):
           ...

        @synchronized('mylock')
        def bar(self, *args):
           ...

    This way only one of either foo or bar can be executing at a time.

    The lock_file_prefix argument is used to provide lock files on disk with a
    meaningful prefix. The prefix should end with a hyphen ('-') if specified.

    The external keyword argument denotes whether this lock should work across
    multiple processes. This means that if two different workers both run a
    a method decorated with @synchronized('mylock', external=True), only one
    of them will execute at a time.

    The lock_path keyword argument is used to specify a special location for
    external lock files to live. If nothing is set, then CONF.lock_path is
    used as a default.
    """

    def wrap(f):

        @functools.wraps(f)
        def inner(*args, **kwargs):
            sem = _semaphores.get(name, semaphore.Semaphore())
            if name not in _semaphores:
                _semaphores[name] = sem
            with sem:
                LOG.debug(_('Got semaphore "%(lock)s" for method "%(method)s"...'), {'lock': name, 'method': f.__name__})
                if not hasattr(local.strong_store, 'locks_held'):
                    local.strong_store.locks_held = []
                local.strong_store.locks_held.append(name)
                try:
                    if external and not CONF.disable_process_locking:
                        LOG.debug(_('Attempting to grab file lock "%(lock)s" for method "%(method)s"...'), {'lock': name, 'method': f.__name__})
                        cleanup_dir = False
                        local_lock_path = lock_path
                        if not local_lock_path:
                            local_lock_path = CONF.lock_path
                        if not local_lock_path:
                            cleanup_dir = True
                            local_lock_path = tempfile.mkdtemp()
                        if not os.path.exists(local_lock_path):
                            fileutils.ensure_tree(local_lock_path)
                        safe_name = name.replace(os.sep, '_')
                        lock_file_name = '%s%s' % (lock_file_prefix, safe_name)
                        lock_file_path = os.path.join(local_lock_path, lock_file_name)
                        try:
                            lock = InterProcessLock(lock_file_path)
                            with lock:
                                LOG.debug(_('Got file lock "%(lock)s" at %(path)s for method "%(method)s"...'), {'lock': name, 'path': lock_file_path, 
                                   'method': f.__name__})
                                retval = f(*args, **kwargs)
                        finally:
                            LOG.debug(_('Released file lock "%(lock)s" at %(path)s for method "%(method)s"...'), {'lock': name, 'path': lock_file_path, 
                               'method': f.__name__})
                            if cleanup_dir:
                                shutil.rmtree(local_lock_path)

                    else:
                        retval = f(*args, **kwargs)
                finally:
                    local.strong_store.locks_held.remove(name)

            return retval

        return inner

    return wrap