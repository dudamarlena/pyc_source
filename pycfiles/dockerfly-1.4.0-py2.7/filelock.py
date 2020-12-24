# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockerfly/contrib/filelock.py
# Compiled at: 2016-06-30 20:54:22
"""
A platform independent file lock that supports the with-statement.
"""
import os, threading, time
try:
    import warnings
except ImportError:
    warnings = None

try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import fcntl
except ImportError:
    fcntl = None

try:
    TimeoutError
except NameError:
    TimeoutError = OSError

__all__ = [
 'Timeout',
 'BaseFileLock',
 'WindowsFileLock',
 'UnixFileLock',
 'SoftFileLock',
 'FileLock']
__version__ = '2.0.6'

class Timeout(TimeoutError):
    """
    Raised when the lock could not be acquired in *timeout*
    seconds.
    """

    def __init__(self, lock_file):
        """
        """
        self.lock_file = lock_file
        return

    def __str__(self):
        temp = ("The file lock '{}' could not be acquired.").format(self.lock_file)
        return temp


class BaseFileLock(object):
    """
    Implements the base class of a file lock.
    """

    def __init__(self, lock_file, timeout=-1):
        """
        """
        self._lock_file = lock_file
        self._lock_file_fd = None
        self.timeout = timeout
        self._thread_lock = threading.Lock()
        self._lock_counter = 0
        return

    @property
    def lock_file(self):
        """
        The path to the lock file.
        """
        return self._lock_file

    @property
    def timeout(self):
        """
        You can set a default timeout for the filelock. It will be used as
        fallback value in the acquire method, if no timeout value (*None*) is
        given.

        If you want to disable the timeout, set it to a negative value.

        A timeout of 0 means, that there is exactly one attempt to acquire the
        file lock.

        .. versionadded:: 2.0.0
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """
        """
        self._timeout = float(value)
        return

    def _acquire(self):
        """
        Platform dependent. If the file lock could be
        acquired, self._lock_file_fd holds the file descriptor
        of the lock file.
        """
        raise NotImplementedError()

    def _release(self):
        """
        Releases the lock and sets self._lock_file_fd to None.
        """
        raise NotImplementedError()

    @property
    def is_locked(self):
        """
        True, if the object holds the file lock.

        .. versionchanged:: 2.0.0

            This was previously a method and is now a property.
        """
        return self._lock_file_fd is not None

    def acquire(self, timeout=None, poll_intervall=0.05):
        """
        Acquires the file lock or fails with a :exc:`Timeout` error.

        .. code-block:: python

            # You can use this method in the context manager (recommended)
            with lock.acquire():
                pass

            # Or you use an equal try-finally construct:
            lock.acquire()
            try:
                pass
            finally:
                lock.release()

        :arg float timeout:
            The maximum time waited for the file lock.
            If ``timeout <= 0``, there is no timeout and this method will
            block until the lock could be acquired.
            If ``timeout`` is None, the default :attr:`~timeout` is used.

        :arg float poll_intervall:
            We check once in *poll_intervall* seconds if we can acquire the
            file lock.

        :raises Timeout:
            if the lock could not be acquired in *timeout* seconds.

        .. versionchanged:: 2.0.0

            This method returns now a *proxy* object instead of *self*,
            so that it can be used in a with statement without side effects.
        """
        if timeout is None:
            timeout = self.timeout
        with self._thread_lock:
            self._lock_counter += 1
        try:
            start_time = time.time()
            while True:
                with self._thread_lock:
                    if not self.is_locked:
                        self._acquire()
                if self.is_locked:
                    break
                elif timeout >= 0 and time.time() - start_time > timeout:
                    raise Timeout(self._lock_file)
                else:
                    time.sleep(poll_intervall)

        except:
            with self._thread_lock:
                self._lock_counter = max(0, self._lock_counter - 1)
            raise

        class ReturnProxy(object):

            def __init__(self, lock):
                self.lock = lock
                return

            def __enter__(self):
                return self.lock

            def __exit__(self, exc_type, exc_value, traceback):
                self.lock.release()
                return

        return ReturnProxy(lock=self)

    def release(self, force=False):
        """
        Releases the file lock.

        Please note, that the lock is only completly released, if the lock
        counter is 0.

        Also note, that the lock file itself is not automatically deleted.

        :arg bool force:
            If true, the lock counter is ignored and the lock is released in
            every case.
        """
        with self._thread_lock:
            if self.is_locked:
                self._lock_counter -= 1
                if self._lock_counter == 0 or force:
                    self._release()
                    self._lock_counter = 0
        return

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return

    def __del__(self):
        self.release(force=True)
        return


class WindowsFileLock(BaseFileLock):
    """
    Uses the :func:`msvcrt.locking` function to hard lock the lock file on
    windows systems.
    """

    def _acquire(self):
        open_mode = os.O_RDWR | os.O_CREAT | os.O_TRUNC
        try:
            fd = os.open(self._lock_file, open_mode)
        except OSError:
            pass
        else:
            try:
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            except (IOError, OSError):
                os.close(fd)
            else:
                self._lock_file_fd = fd

        return

    def _release(self):
        fd = self._lock_file_fd
        self._lock_file_fd = None
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        os.close(fd)
        try:
            os.remove(self._lock_file)
        except OSError:
            pass

        return


class UnixFileLock(BaseFileLock):
    """
    Uses the :func:`fcntl.flock` to hard lock the lock file on unix systems.
    """

    def _acquire(self):
        open_mode = os.O_RDWR | os.O_CREAT | os.O_TRUNC
        fd = os.open(self._lock_file, open_mode)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (IOError, OSError):
            os.close(fd)
        else:
            self._lock_file_fd = fd

        return

    def _release(self):
        fd = self._lock_file_fd
        self._lock_file_fd = None
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
        return


class SoftFileLock(BaseFileLock):
    """
    Simply watches the existence of the lock file.
    """

    def _acquire(self):
        open_mode = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC
        try:
            fd = os.open(self._lock_file, open_mode)
        except (IOError, OSError):
            pass
        else:
            self._lock_file_fd = fd

        return

    def _release(self):
        os.close(self._lock_file_fd)
        self._lock_file_fd = None
        try:
            os.remove(self._lock_file)
        except OSError:
            pass

        return


FileLock = None
if msvcrt:
    FileLock = WindowsFileLock
else:
    FileLock = SoftFileLock