# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\gui\events.py
# Compiled at: 2013-12-11 23:17:46
"""
Event type definitions and threading code for background jobs

Copyright (C) 2012 Daniel Meliza <dmeliza@dylan.uchicago.edu>
Created 2012-02-16
"""
import wx, threading
from chirp.common.progress import consumer
myEVT_STAGE = wx.NewEventType()
EVT_STAGE = wx.PyEventBinder(myEVT_STAGE, 1)
myEVT_COUNT = wx.NewEventType()
EVT_COUNT = wx.PyEventBinder(myEVT_COUNT, 1)

class BatchEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""

    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        return self._value


class BatchConsumer(consumer):
    """
    Objects of this class monitor a queue and produces events as the
    batch job progresses.  For ease in passing this task to another
    thread, the start method returns immediately; call the object to
    start consuming.
    """

    def __init__(self, parent):
        self._parent = parent

    def start(self, queue, nworkers, stop_signal, njobs=None, gen=None):
        self.queue = queue
        self.nworkers = nworkers
        self.stop_signal = stop_signal
        self.njobs = njobs
        self.gen = gen

    def __call__(self):
        consumer.start(self, self.queue, self.nworkers, self.stop_signal, self.njobs, self.gen)

    def process(self, index, value):
        evt = BatchEvent(myEVT_COUNT, -1, index)
        wx.PostEvent(self._parent, evt)

    def finish(self, lastindex):
        evt = BatchEvent(myEVT_COUNT, -1, None)
        wx.PostEvent(self._parent, evt)
        return

    def stop(self):
        self.stop_signal.value = True