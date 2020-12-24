# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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