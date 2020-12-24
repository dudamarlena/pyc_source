# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madeiracloud/Watcher.py
# Compiled at: 2011-12-16 02:01:38
import time, signal, asyncore, threading, pyinotify

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        print 'Creating:', event.pathname

    def process_IN_DELETE(self, event):
        print 'Removing:', event.pathname


def run():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_MODIFY
    notifier = pyinotify.AsyncNotifier(wm, EventHandler())
    wm.add_watch('/etc/host.conf', mask, rec=True)
    wm.add_watch('/etc/nssolve.conf', mask, rec=True)
    asyncore.loop()