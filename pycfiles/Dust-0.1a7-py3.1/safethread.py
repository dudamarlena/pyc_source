# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/util/safethread.py
# Compiled at: 2010-05-18 00:44:19
import traceback
from threading import Thread, Event

def waitForEvent(event):
    while not event.isSet():
        event.wait(1000)


def waitFor(delay):
    import time
    time.sleep(delay)


def wait():
    import time
    while True:
        time.sleep(1000)


class SafeThread(Thread):

    def __init__(self, target=None, args=None):
        self.method = target
        self.args = args
        Thread.__init__(self, target=self.safeCall)

    def safeCall(self):
        if self.method == None:
            return
        else:
            try:
                if self.args == None:
                    self.method()
                else:
                    self.method(*self.args)
            except Exception:
                print('Internal crash')
                traceback.print_exc()

            return