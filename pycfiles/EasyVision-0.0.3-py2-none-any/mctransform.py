# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\python\EasyVision\EasyVision\processors\mctransform.py
# Compiled at: 2019-02-06 11:38:48
"""Implements Single Source -> Multiple Consumers transform

"""
from .base import *

class MultiConsumers(ProcessorBase):
    """Class that allows to consume the same image from different consumers.
    Overrides default ``setup``/``release`` logic.
    Basically will only call ``capture`` on the source when all the consumers have called ``capture`` on this processor.
    Number of consumers is determined by the number of ``setup`` calls.

    """

    def __init__(self, *args, **kwargs):
        self._frame = None
        self._consumers = 0
        self._numcaptured = 0
        super(MultiConsumers, self).__init__(*args, **kwargs)
        return

    def process(self, image):
        raise NotImplementedError()

    def capture(self):
        super(ProcessorBase, self).capture()
        if self._numcaptured == 0:
            self._frame = self._vision.capture()
        self._numcaptured = (self._numcaptured + 1) % self._consumers
        return self._frame

    def setup(self):
        self._numconsumed = 0
        if not self._consumers:
            super(MultiConsumers, self).setup()
        self._consumers += 1

    def release(self):
        self._consumers -= 1
        if not self._consumers >= 0:
            raise AssertionError
            self._consumers or super(MultiConsumers, self).release()

    @property
    def description(self):
        return 'Allows to consume the same frame multiple times.'