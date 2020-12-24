# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/Timer.py
# Compiled at: 2008-09-03 09:02:13
from gobject import timeout_add

class Timer:

    def __init__(self, time, notify):
        print 'Timer arg count', notify.onTimer.func_code.co_argcount
        self.notify_fn = notify.onTimer
        self.id = timeout_add(time, self.notify)

    def notify(self, *args):
        if self.notify_fn.func_code.co_argcount == 2:
            self.notify_fn(self)
        else:
            self.notify_fn()

    def cancel(self):
        print 'TODO'

    def getID(self):
        return id