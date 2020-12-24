# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/tqdm/tqdm/_monitor.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3676 bytes
from threading import Event, Thread, current_thread
from time import time
from warnings import warn
import atexit
__all__ = [
 'TMonitor', 'TqdmSynchronisationWarning']

class TqdmSynchronisationWarning(RuntimeWarning):
    __doc__ = 'tqdm multi-thread/-process errors which may cause incorrect nesting\n    but otherwise no adverse effects'


class TMonitor(Thread):
    __doc__ = '\n    Monitoring thread for tqdm bars.\n    Monitors if tqdm bars are taking too much time to display\n    and readjusts miniters automatically if necessary.\n\n    Parameters\n    ----------\n    tqdm_cls  : class\n        tqdm class to use (can be core tqdm or a submodule).\n    sleep_interval  : fload\n        Time to sleep between monitoring checks.\n    '
    _time = None
    _event = None

    def __init__(self, tqdm_cls, sleep_interval):
        Thread.__init__(self)
        self.daemon = True
        self.was_killed = Event()
        self.woken = 0
        self.tqdm_cls = tqdm_cls
        self.sleep_interval = sleep_interval
        if TMonitor._time is not None:
            self._time = TMonitor._time
        else:
            self._time = time
        if TMonitor._event is not None:
            self._event = TMonitor._event
        else:
            self._event = Event
        atexit.register(self.exit)
        self.start()

    def exit(self):
        self.was_killed.set()
        if self is not current_thread():
            self.join()
        return self.report()

    def get_instances(self):
        return [i for i in self.tqdm_cls._instances.copy() if hasattr(i, 'start_t')]

    def run(self):
        cur_t = self._time()
        while True:
            self.woken = cur_t
            self.was_killed.wait(self.sleep_interval)
            if self.was_killed.is_set():
                return
            with self.tqdm_cls.get_lock():
                cur_t = self._time()
                instances = self.get_instances()
                for instance in instances:
                    if self.was_killed.is_set():
                        return
                    if instance.miniters > 1 and cur_t - instance.last_print_t >= instance.maxinterval:
                        instance.miniters = 1
                        instance.refresh(nolock=True)

                if instances != self.get_instances():
                    warn('Set changed size during iteration (see https://github.com/tqdm/tqdm/issues/481)', TqdmSynchronisationWarning)

    def report(self):
        return not self.was_killed.is_set()