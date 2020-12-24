# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/concurrent/monitor.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 5900 bytes
import collections, copy, threading, typing as tp
from ..decorators import wraps
__all__ = [
 'Monitor', 'RMonitor', 'MonitorDict', 'MonitorList']
K, V, T = tp.TypeVar('K'), tp.TypeVar('V'), tp.TypeVar('T')

class Monitor:
    __doc__ = '\n    Base utility class for creating monitors (the synchronization thingies!)\n\n    These are NOT re-entrant!\n\n    Use it like that:\n\n    >>> class MyProtectedObject(Monitor):\n    >>>     def __init__(self, *args, **kwargs):\n    >>>         Monitor.__init__(self)\n    >>>         ... do your job ..\n\n    >>>     @Monitor.synchronized\n    >>>     def function_that_needs_mutual_exclusion(self):\n    >>>         .. do your threadsafe jobs ..\n\n    >>>     def function_that_partially_needs_protection(self):\n    >>>         .. do your jobs ..\n    >>>         with Monitor.acquire(self):\n    >>>             .. do your threadsafe jobs ..\n    >>>         .. do your jobs ..\n    >>>         with self:\n    >>>             .. do your threadsafe jobs ..\n    '
    __slots__ = ('_monitor_lock', )

    def __enter__(self):
        self._monitor_lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._monitor_lock.release()
        return False

    def __init__(self):
        """You need to invoke this at your constructor
        You can also use it to release locks of other objects."""
        self._monitor_lock = threading.Lock()

    @staticmethod
    def synchronized(fun):
        """
        This is a decorator. Class method decorated with that will lock the
        global lock of given instance, making it threadsafe. Depending on
        usage pattern of your class and it's data semantics, your performance
        may vary
        """

        @wraps(fun)
        def monitored(*args, **kwargs):
            with args[0]._monitor_lock:
                return fun(*args, **kwargs)

        return monitored

    class release:
        __doc__ = "\n        Returns a context manager object that can release another object\n        as long as that object is a monitor.\n\n        Consider foo, which is a monitor. You have a protected function,\n        but you feel that you can release it for a while as it would\n        improve parallelism. You can use it as such:\n\n        >>> @Monitor.synchronized\n        >>> def protected_function(self):\n        >>>     .. do some stuff that needs mutual exclusion ..\n        >>>     with Monitor.release(self):\n        >>>         .. do some I/O that doesn't need mutual exclusion ..\n        >>>     .. back to protected stuff ..\n        "

        def __init__(self, foo: 'Monitor'):
            self.foo = foo

        def __enter__(self):
            self.foo._monitor_lock.release()

        def __exit__(self, e1, e2, e3):
            self.foo._monitor_lock.acquire()
            return False

    class acquire:
        __doc__ = '\n        Returns a context manager object that can lock another object,\n        as long as that object is a monitor.\n\n        Consider foo, which is a monitor. If you needed to lock it from\n        outside, you would do:\n\n        >>> with Monitor.acquire(foo):\n        >>>     .. do operations on foo that need mutual exclusion ..\n        '

        def __init__(self, foo: 'Monitor'):
            self.foo = foo

        def __enter__(self):
            self.foo._monitor_lock.acquire()

        def __exit__(self, e1, e2, e3):
            self.foo._monitor_lock.release()
            return False

    @classmethod
    def synchronize_on(cls, monitor):
        """
        A decorator for locking on non-self Monitor objects

        Use it like:

        >>> class MasterClass(Monitor):
        >>>     def get_object(self):
        >>>         class SlaveClass:
        >>>             @Monitor.synchronize_on(self)
        >>>             def get_object(self2):
        >>>                 ...
        >>>         return SlaveClass
        """

        def outer(fun):

            @wraps(fun)
            def inner(*args, **kwargs):
                with cls.acquire(monitor):
                    return fun(*args, **kwargs)

            return inner

        return outer


class RMonitor(Monitor):
    __doc__ = '\n    Monitor, but using an reentrant lock instead of a normal one\n    '

    def __init__(self):
        self._monitor_lock = threading.RLock()


class MonitorList(tp.Generic[T], collections.UserList, Monitor):
    __doc__ = 'A list that is also a monitor'

    def __init__(self, *args):
        (collections.UserList.__init__)(self, *args)
        Monitor.__init__(self)

    def __copy__(self):
        return MonitorList(copy.copy(self.data))

    def __deepcopy__(self, memo):
        return MonitorList(copy.deepcopy(self.data, memo))

    def __getitem__(self, item: tp.Union[(slice, int)]) -> T:
        return self.data[item]

    def __setitem__(self, key: int, value: T) -> None:
        self.data[key] = value

    def __delitem__(self, key: tp.Union[(slice, int)]) -> None:
        del self.data[key]


class MonitorDict(tp.Generic[(K, V)], collections.UserDict, Monitor):
    __doc__ = 'A dict that is also a monitor'

    def __init__(self, *args, **kwargs):
        (collections.UserDict.__init__)(self, *args, **kwargs)
        Monitor.__init__(self)

    def __getitem__(self, item: K) -> V:
        return self.data[item]

    def __setitem__(self, key: K, value: V) -> None:
        self.data[key] = value

    def __delitem__(self, key: K) -> None:
        del self.data[key]

    def __copy__(self):
        return MonitorDict(copy.copy(self.data))

    def __deepcopy__(self, memo):
        return MonitorDict(copy.deepcopy(self.data, memo))