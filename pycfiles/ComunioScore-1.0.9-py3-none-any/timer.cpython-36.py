# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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