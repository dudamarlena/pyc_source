# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/frameworks/events/subscribers.py
# Compiled at: 2016-02-25 04:17:16
import threading

class BlockSubscriber(object):
    """
    Block until event happend
    """

    def __init__(self, checker=None):
        self.block_cond = threading.Condition()
        self.checker = checker or (lambda *a, **k: True)

    def __call__(self, *args, **kwg):
        if not self.checker(*args, **kwg):
            return
        with self.block_cond:
            self.block_cond.notify()

    def wait(self, timeout=None):
        """
        Wait until event happend
        """
        with self.block_cond:
            self.block_cond.wait(timeout)