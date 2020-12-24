# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/throttle.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 7302 bytes
from __future__ import absolute_import
from builtins import object
import time, threading
from toil.lib.threading import BoundedEmptySemaphore

class GlobalThrottle(object):
    __doc__ = '\n    A thread-safe rate limiter that throttles all threads globally. This should be used to\n    regulate access to a global resource. It can be used as a function/method decorator or as a\n    simple object, using the throttle() method. The token generation starts with the first call\n    to throttle() or the decorated function. Each subsequent call to throttle() will then acquire\n    a token, possibly having to wait until one becomes available. The number of unused tokens\n    will not exceed a limit given at construction time. This is a very basic mechanism to\n    prevent the resource from becoming swamped after longer pauses.\n    '

    def __init__(self, min_interval, max_unused):
        self.min_interval = min_interval
        self.semaphore = BoundedEmptySemaphore(max_unused)
        self.thread_start_lock = threading.Lock()
        self.thread_started = False
        self.thread = threading.Thread(target=(self.generator))
        self.thread.daemon = True

    def generator(self):
        while True:
            try:
                self.semaphore.release()
            except ValueError:
                pass

            time.sleep(self.min_interval)

    def throttle(self, wait=True):
        """
        If the wait parameter is True, this method returns True after suspending the current
        thread as necessary to ensure that no less than the configured minimum interval passed
        since the most recent time an invocation of this method returned True in any thread.

        If the wait parameter is False, this method immediatly returns True if at least the
        configured minimum interval has passed since the most recent time this method returned
        True in any thread, or False otherwise.
        """
        with self.thread_start_lock:
            if not self.thread_started:
                self.thread.start()
                self.thread_started = True
        return self.semaphore.acquire(blocking=wait)

    def __call__(self, function):

        def wrapper(*args, **kwargs):
            self.throttle()
            return function(*args, **kwargs)

        return wrapper


class LocalThrottle(object):
    __doc__ = '\n    A thread-safe rate limiter that throttles each thread independently. Can be used as a\n    function or method decorator or as a simple object, via its .throttle() method.\n\n    The use as a decorator is deprecated in favor of throttle().\n    '

    def __init__(self, min_interval):
        """
        Initialize this local throttle.

        :param min_interval: The minimum interval in seconds between invocations of the throttle
        method or, if this throttle is used as a decorator, invocations of the decorated method.
        """
        self.min_interval = min_interval
        self.per_thread = threading.local()
        self.per_thread.last_invocation = None

    def throttle(self, wait=True):
        """
        If the wait parameter is True, this method returns True after suspending the current
        thread as necessary to ensure that no less than the configured minimum interval has
        passed since the last invocation of this method in the current thread returned True.

        If the wait parameter is False, this method immediatly returns True (if at least the
        configured minimum interval has passed since the last time this method returned True in
        the current thread) or False otherwise.
        """
        now = time.time()
        last_invocation = self.per_thread.last_invocation
        if last_invocation is not None:
            interval = now - last_invocation
            if interval < self.min_interval:
                if wait:
                    remainder = self.min_interval - interval
                    time.sleep(remainder)
                else:
                    return False
        self.per_thread.last_invocation = now
        return True

    def __call__(self, function):

        def wrapper(*args, **kwargs):
            self.throttle()
            return function(*args, **kwargs)

        return wrapper


class throttle(object):
    __doc__ = "\n    A context manager for ensuring that the execution of its body takes at least a given amount\n    of time, sleeping if necessary. It is a simpler version of LocalThrottle if used as a\n    decorator.\n\n    Ensures that body takes at least the given amount of time.\n\n    >>> start = time.time()\n    >>> with throttle(1):\n    ...     pass\n    >>> 1 <= time.time() - start <= 1.1\n    True\n\n    Ditto when used as a decorator.\n\n    >>> @throttle(1)\n    ... def f():\n    ...     pass\n    >>> start = time.time()\n    >>> f()\n    >>> 1 <= time.time() - start <= 1.1\n    True\n\n    If the body takes longer by itself, don't throttle.\n\n    >>> start = time.time()\n    >>> with throttle(1):\n    ...     time.sleep(2)\n    >>> 2 <= time.time() - start <= 2.1\n    True\n\n    Ditto when used as a decorator.\n\n    >>> @throttle(1)\n    ... def f():\n    ...     time.sleep(2)\n    >>> start = time.time()\n    >>> f()\n    >>> 2 <= time.time() - start <= 2.1\n    True\n\n    If an exception occurs, don't throttle.\n\n    >>> start = time.time()\n    >>> try:\n    ...     with throttle(1):\n    ...         raise ValueError('foo')\n    ... except ValueError:\n    ...     end = time.time()\n    ...     raise\n    Traceback (most recent call last):\n    ...\n    ValueError: foo\n    >>> 0 <= end - start <= 0.1\n    True\n\n    Ditto when used as a decorator.\n\n    >>> @throttle(1)\n    ... def f():\n    ...     raise ValueError('foo')\n    >>> start = time.time()\n    >>> try:\n    ...     f()\n    ... except ValueError:\n    ...     end = time.time()\n    ...     raise\n    Traceback (most recent call last):\n    ...\n    ValueError: foo\n    >>> 0 <= end - start <= 0.1\n    True\n    "

    def __init__(self, min_interval):
        self.min_interval = min_interval

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            duration = time.time() - self.start
            remainder = self.min_interval - duration
            if remainder > 0:
                time.sleep(remainder)

    def __call__(self, function):

        def wrapper(*args, **kwargs):
            with self:
                return function(*args, **kwargs)

        return wrapper