# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utilThreading/managerThread.py
# Compiled at: 2017-08-14 04:52:37
# Size of source mod 2**32: 2942 bytes
"""
------------------------------------------------------------------------------
Name:        managerThread
Author:      Sean Wiseman
------------------------------------------------------------------------------
"""
from time import sleep
from inspect import signature
import threading
try:
    import Queue as queue
except ImportError:
    import queue

__version__ = '1.0.0'

class ManagerThread(object):
    __doc__ = 'A utility Thread wrapper which starts a thread that manages\n        a queue and passes queue entries to be processed a by user\n        defined function.\n    '
    instances = []

    def __init__(self, name='ManagerThreadInstance', target_func=None, timeout=0.1, daemon=True, *args, **kwargs):
        """
        args:
            name        --
            target_func --
            log_q       --
            timeout     --
            daemon      --
        """
        ManagerThread.instances.append(self)
        self.name = name
        self._ManagerThread__alive = False
        self._ManagerThread__lock = threading.Lock()
        self.queue = queue.Queue()
        self._ManagerThread__timeout = timeout
        self.target_func = self.assign_target_func(target_func)
        self.worker_thread = threading.Thread(target=self._ManagerThread__worker, name=self.name)
        self.worker_thread.daemon = daemon

    def is_alive(self):
        return self._ManagerThread__alive

    @staticmethod
    def assign_target_func(func):
        """Make sure func is a callable object that accepts args"""
        if callable(func) and len(signature(func).parameters):
            return func
        raise ValueError('Target function is not callable')

    def start(self):
        self._ManagerThread__alive = True
        self.worker_thread.start()

    def stop(self):
        """ stop worker thread """
        self._ManagerThread__alive = False

    def __worker(self):
        """Watches self.queue and executes
        self.target_func on delivery of new data
        """
        while self._ManagerThread__alive:
            try:
                sleep(self._ManagerThread__timeout)
                data = self.queue.get(block=False)
            except queue.Empty:
                pass
            else:
                try:
                    try:
                        self._ManagerThread__lock.acquire()
                        self.target_func(data)
                        sleep(self._ManagerThread__timeout)
                    except Exception as err:
                        raise err

                finally:
                    self._ManagerThread__lock.release()

    @classmethod
    def start_all_threads(cls):
        for thread in cls.instances:
            thread.start()

    @classmethod
    def stop_all_threads(cls):
        for thread in cls.instances:
            thread.stop()

    @classmethod
    def thread_statuses(cls):
        return {t.name:t._ManagerThread__alive for t in cls.instances}


if __name__ == '__main__':
    pass