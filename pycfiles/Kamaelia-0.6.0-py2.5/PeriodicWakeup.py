# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Grey/PeriodicWakeup.py
# Compiled at: 2008-10-19 12:19:52
import time, Axon

class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 300
    message = 'tick'

    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send(self.message, 'outbox')


__kamaelia_components__ = (PeriodicWakeup,)