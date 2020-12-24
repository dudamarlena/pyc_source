# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/threads/runnable.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 4029 bytes
from .. import log
import contextlib, functools, threading, time, traceback, queue

class Runnable:
    __doc__ = '\n    Base class for all objects that contain threads - including threads\n    created and started by bp code, and threads started by external libraries.\n\n    There are three possible thread categories for a Runnable:\n\n    1. Runs on the master thread - M\n    2. A new thread created by us - N\n    3. A new external thread created by some third-party code - X\n\n    Case X is tricky because we would like our code to be called at the start of\n    the new thread, and again at the end of that thread, but we can\'t.\n\n    Lifecycle - what a Runnable does, and what threads it could be called on\n\n    * construction: M\n    * start: M\n    * on_start: M\n      * called on the master thread after any new thread has started up\n    * run: MN\n    * callbacks: MNX\n    * join: M\n    * cleanup: M(N?)\n\n    TODO: right now we run all our cleanups on the new thread, if there is a new\n    thread, otherwise on the master thread.  Should we move to doing all the\n    cleanups on the master thread?\n\n    The way to use a Runnable is like a context manager:\n\n    with some_runnable() as runnable:\n         add_some_callbacks(runnable)\n         more_stuff_that_runs_on_start()\n\n         # Depending on the thread category, the `Runnable` isn\'t guaranteed to\n         # actually "go off" until the end of this block.\n\n    We\'re going to call the code inside the context manager `on_start`\n\n    '
    MASTER, NEW, EXTERNAL = ('M', 'N', 'X')
    category = NEW
    timeout = 0.1

    def __init__(self):
        self.run_event = threading.Event()
        self.stop_event = threading.Event()

    @property
    def running(self):
        """
        Is this Runnable expected to make any progress from here?

        The Runnable might still execute a little code after it has stopped
        running.
        """
        return self.run_event.is_set() and not self.stop_event.is_set()

    def is_alive(self):
        """
        Is this Runnable still executing code?

        In some cases, such as threads, self.is_alive() might be true for some
        time after self.running has turned False.
        """
        return self.running

    def start(self):
        self.run_event.set()

    def stop(self):
        self.stop_event.set()

    def wait(self):
        self.stop_event.wait()

    def cleanup(self):
        """
        Cleans up resources after the Runnable.

        self.cleanup() may not throw an exception.
        """
        pass

    def run(self):
        try:
            try:
                while self.running:
                    self.run_once()

            except:
                log.error('Exception at %s: \n%s', str(self), traceback.format_exc())

        finally:
            self.stop()
            self.cleanup()

    def run_once(self):
        """The target code that is repeatedly executed in the run method"""
        pass

    @contextlib.contextmanager
    def run_until_stop(self):
        """
        A context manager that starts this Runnable, yields,
        and then waits for it to finish."""
        self.start()
        try:
            yield self
        finally:
            self.stop()

        self.wait()


class LoopThread(Runnable):

    def __init__(self, daemon=True, **kwds):
        super().__init__()
        self.thread = (threading.Thread)(daemon=daemon, target=self.run, **kwds)

    def start(self):
        self.thread.start()

    def run(self):
        super().start()
        super().run()

    def is_alive(self):
        return self.thread.is_alive()


class QueueHandler(LoopThread):

    def __init__(self, timeout=0.1, send=None, **kwds):
        (super().__init__)(**kwds)
        self.timeout = timeout
        self.queue = queue.Queue()
        self.send = send or self.send

    def run_once(self):
        try:
            msg = self.queue.get(timeout=(self.timeout))
        except queue.Empty:
            pass
        else:
            self.send(msg)

    def send(self, msg):
        pass