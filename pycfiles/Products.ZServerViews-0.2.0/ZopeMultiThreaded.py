# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/timers/ZopeMultiThreaded/ZopeMultiThreaded.py
# Compiled at: 2015-07-18 19:40:58
from threading import Thread
import AccessControl, transaction
from Products.ZScheduler.timers.ZopeSingleThreaded.ZopeSingleThreaded import ZopeSingleThreaded

class ZopeMultiThreaded(ZopeSingleThreaded):
    """
    Timer thread kicks off job(s) in their own detached thread.

    This has the benefit of most accurately maintaining job start times
    as the timer is not delayed in the task of dispatch by performing
    potentially long-running schedule events.
    """
    meta_type = 'ZopeMultiThreaded'

    def _dispatch(self, event):
        worker = Thread(None, self._invokeFromPath, [('/').join(event.getPhysicalPath())])
        worker.setName(event.getId())
        worker.setDaemon(1)
        worker.start()
        return

    def _invokeFromPath(self, event_path):
        conn = Globals.DB.open()
        app = self._getContext(conn.root()['Application'])
        app.unrestrictedTraverse(event_path).manage_invokeEvent()
        transaction.get().commit()
        conn.close()


AccessControl.class_init.InitializeClass(ZopeMultiThreaded)