# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskillscore/thread_handler.py
# Compiled at: 2017-08-07 09:44:23
""" Thread handler. """
import threading, time
from .singleton import Singleton
from .usb_utils import USB

class ThreadHandler(Singleton):
    """ Thread handler. """

    def __init__(self):
        """ Initialisation. """
        self.thread_pool = []
        self.run_events = []

    def run(self, target, args=()):
        """ Run a function in a separate thread.

        :param target: the function to run.
        :param args: the parameters to pass to the function.
        """
        run_event = threading.Event()
        run_event.set()
        thread = threading.Thread(target=target, args=args + (run_event,))
        self.thread_pool.append(thread)
        self.run_events.append(run_event)
        thread.start()

    def start_run_loop(self):
        """ Start the thread handler, ensuring that everything stops property
            when sending a keyboard interrup.
        """
        try:
            while 1:
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """ Stop all functions running in the thread handler."""
        for run_event in self.run_events:
            run_event.clear()

        for thread in self.thread_pool:
            thread.join()