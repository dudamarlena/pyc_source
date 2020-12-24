# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/cancellable_thread.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1539 bytes
import logging
logger = logging.getLogger(__name__)
from threading import Thread, Event

class CancellableThread(Thread):
    __doc__ = '\n        Class for use by ThreadedTaskBox.\n    '

    def __init__(self, run_function, on_complete):
        Thread.__init__(self)
        self.setDaemon(True)
        self.run_function = run_function
        self.on_complete = on_complete
        self._CancellableThread__stop = Event()
        self._CancellableThread__cancel = Event()

    def run(self):
        try:
            data = self.run_function(stop=(self._CancellableThread__stop))
            if not self._CancellableThread__cancel.is_set():
                self.on_complete(data)
        except KeyboardInterrupt:
            self.cancel()
        except:
            logger.exception('Unhandled exception in CancellableThread run()')

    def stop(self):
        """
            Stops the thread, and calls the on_complete callback
        """
        self._CancellableThread__stop.set()

    def cancel(self):
        """
            Stops the thread, and does not call the on_complete callback.
        """
        self._CancellableThread__cancel.set()
        self._CancellableThread__stop.set()