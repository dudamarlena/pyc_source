# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/utils/timer.py
# Compiled at: 2020-03-29 20:59:07
# Size of source mod 2**32: 883 bytes
import logging, threading, functools

class PeriodicTimer:

    def __init__(self, interval, callback):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('create class PeriodicTimer')
        self.interval = interval

        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if result:
                self.thread = threading.Timer(self.interval, self.callback)
                self.thread.start()

        self.callback = wrapper

    def start(self):
        """ starts the PeriodicTimer thread

        """
        self.thread = threading.Timer(self.interval, self.callback)
        self.thread.start()

    def cancel(self):
        """  cancels the PeriodicTimer thread

        """
        self.thread.cancel()