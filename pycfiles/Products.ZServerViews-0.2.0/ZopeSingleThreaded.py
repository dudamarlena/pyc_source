# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/timers/ZopeSingleThreaded/ZopeSingleThreaded.py
# Compiled at: 2015-07-18 19:40:58
import AccessControl, transaction
from Products.ZScheduler.interfaces.ITimer import ITimer
from threading import Thread
from DateTime import DateTime
from Acquisition import aq_base
from Products.ZScheduler.timers.Base import ThreadedTimer
worker = None

class ZopeSingleThreaded(ThreadedTimer):
    """
    A single-threaded timer which goes to sleep, waking to fire the next event in the queue
    """
    meta_type = 'ZopeSingleThreaded'

    def _load(self):
        while 1:
            event = scheduler.nextEvent()
            while event:
                now = DateTime()
                e_time = event.time.timeTime()
                interval = e_time - now.timeTime()
                scheduler.semaphore.wait(interval)
                now = DateTime()
                if e_time - now.timeTime() <= 0:
                    self._dispatch(event)

    def _dispatch(self, event):
        """
        overrideable dispatching driver
        """
        event.manage_invokeEvent()
        transaction.get().commit()


AccessControl.class_init.InitializeClass(ZopeSingleThreaded)