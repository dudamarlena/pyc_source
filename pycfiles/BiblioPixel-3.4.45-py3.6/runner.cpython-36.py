# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/builder/runner.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1653 bytes
import traceback, weakref
from ..util import log
from ..util.threads import runnable

class Runner:
    __doc__ = '\n    Class that makes sure that a single builder is running.\n    '

    def __init__(self, builder):
        self.thread = None
        self.is_running = False
        self.builder = weakref.ref(builder)

    def start(self, threaded):
        """Creates and starts the project."""
        self.stop()
        self.__class__._INSTANCE = weakref.ref(self)
        self.is_running = True
        if threaded:
            self.thread = runnable.LoopThread()
            self.thread.run_once = self._target
            self.thread.start()
        else:
            self._target()

    def stop(self):
        """
        Stop the Runner if it's running.
        Called as a classmethod, stop the running instance if any.
        """
        if self.is_running:
            log.info('Stopping')
            self.is_running = False
            self.__class__._INSTANCE = None
            try:
                self.thread and self.thread.stop()
            except:
                log.error('Error stopping thread')
                traceback.print_exc()

            self.thread = None
            return True

    @classmethod
    def instance(cls):
        """Return the unique instance of Runner, if any, or None"""
        return cls._INSTANCE and cls._INSTANCE()

    _INSTANCE = None

    def _target(self):
        try:
            try:
                self.builder()._run()
            except:
                if self.thread:
                    log.error(traceback.format_exc())
                raise

        finally:
            b = self.builder()
            b and b.stop()