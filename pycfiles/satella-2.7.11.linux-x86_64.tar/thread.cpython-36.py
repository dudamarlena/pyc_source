# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/concurrent/thread.py
# Compiled at: 2020-04-22 08:35:40
# Size of source mod 2**32: 5051 bytes
import ctypes, platform, threading, typing as tp
from threading import Condition as PythonCondition
from satella.time import measure
from ...exceptions import ResourceLocked, WouldWaitMore

class Condition(PythonCondition):
    __doc__ = "\n    A wrapper to faciliate easier usage of Pythons' threading.Condition.\n\n    There's no need to acquire the underlying lock, as wait/notify/notify_all do it for you.\n    "

    def wait(self, timeout=None):
        """
        Wait for condition to become true.

        :param timeout: timeout to wait. None is default and means infinity
        :raises ResourceLocked: unable to acquire the lock within specified timeout.
        :raises WouldWaitMore: wait's timeout has expired
        """
        with measure() as (measurement):
            if timeout is None:
                self.acquire()
            else:
                if not self.acquire(timeout=timeout):
                    raise ResourceLocked('internal lock locked')
            try:
                if timeout is None:
                    super().wait()
                else:
                    if not super().wait(timeout=(timeout - measurement())):
                        raise WouldWaitMore('wait was not notified')
            finally:
                self.release()

    def notify_all(self):
        """
        Notify all threads waiting on this Condition
        """
        with self._lock:
            super().notify_all()

    def notify(self, n=1):
        """
        Notify n threads waiting on this Condition

        :param n: amount of threads to notify
        """
        with self._lock:
            super().notify(n=n)


class TerminableThread(threading.Thread):
    __doc__ = "\n    Class that will execute something in a loop unless terminated. Use like:\n\n    >>> class MeGrimlock(TerminableThread):\n    >>>     def loop(self):\n    >>>         ... do your operations ..\n    >>> a = MeGrimlock()\n    >>> a.start()\n    >>> a.terminate().join()\n\n    Flag whether to terminate is stored in **self._terminating**.\n\n    If you decide to override run(), you got to check periodically for **self._terminating** to\n    become true.\n    If you decide to use the loop/cleanup interface, you don't need to do so.\n\n    You may also use it as a context manager. Entering the context will start the thread, and\n    exiting it will .terminate().join() it, in the following way:\n\n    >>> a = MeGrimlock()\n    >>> with a:\n    >>>     ...\n    >>> self.assertFalse(a.is_alive())\n    "
    __slots__ = ('_terminating', )

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._terminating = False

    def loop(self) -> None:
        """
        Run one iteration of the loop. Meant to be overrided. You do not need to override it
        if you decide to override run() through.

        This should block for as long as a single check will take, as termination checks take place
        between calls.
        """
        pass

    def run(self) -> None:
        """
        Calls self.loop() indefinitely, until terminating condition is met
        """
        while not self._terminating:
            self.loop()

        self.cleanup()

    def cleanup(self):
        """
        Called after thread non-forced termination, in the thread's context.

        The default implementation does nothing.
        """
        pass

    def __enter__(self):
        """Returns self"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate().join()
        return False

    def terminate(self, force: bool=False) -> 'TerminableThread':
        """
        Signal this thread to terminate.

        Forcing, if requested, will be done by injecting a SystemExit exception into target
        thread, so the thread must acquire GIL. For example, following would not be interruptable:

        >>> time.sleep(1000000)

        Note that calling force=True on PyPy won't work, and NotImplementedError will be raised
        instead.

        :param force: Whether to force a quit
        :return: self
        :raises RuntimeError: when something goes wrong with the underlying Python machinery
        :raises NotImplementedError: force=True was used on PyPy
        """
        self._terminating = True
        if force:
            if platform.python_implementation() == 'PyPy':
                raise NotImplementedError('force=True was made on PyPy')
            ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._ident), ctypes.py_object(SystemExit))
            if ret == 0:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._ident), 0)
                raise RuntimeError('Zero threads killed!')
            elif ret > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._ident), 0)
                raise RuntimeError('Multiple threads killed!')
        return self