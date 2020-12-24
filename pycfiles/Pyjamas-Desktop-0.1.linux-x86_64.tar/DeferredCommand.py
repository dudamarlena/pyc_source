# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/DeferredCommand.py
# Compiled at: 2008-09-03 09:02:13
from Timer import Timer
deferredCommands = []
timerIsActive = False

class DeferredCommand:

    def add(self, cmd):
        global deferredCommands
        deferredCommands.append(cmd)
        self.maybeSetDeferredCommandTimer()

    def flushDeferredCommands(self):
        for i in range(len(deferredCommands)):
            current = deferredCommands[0]
            del deferredCommands[0]
            if current == None:
                return
            else:
                current.execute()

        return

    def maybeSetDeferredCommandTimer(self):
        global timerIsActive
        if not timerIsActive and not len(deferredCommands) == 0:
            Timer(1, self)
            timerIsActive = True

    def onTimer(self, sender):
        global timerIsActive
        self.flushDeferredCommands()
        timerIsActive = False
        self.maybeSetDeferredCommandTimer()