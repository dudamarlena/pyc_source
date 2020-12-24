# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/background.py
# Compiled at: 2008-10-19 12:19:52
"""

Out of the original code for background, this seems the most likely to
remain intact.

"""
from Scheduler import scheduler
from Component import component
import threading, CoordinatingAssistantTracker as cat

class background(threading.Thread):
    """A python thread which runs a scheduler. Takes the same arguments at creation that scheduler.run.runThreads accepts."""
    lock = threading.Lock()

    def __init__(self, slowmo=0, zap=False):
        if not background.lock.acquire(False):
            raise 'only one scheduler for now can be run!'
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.zap = zap

    def run(self):
        if self.zap:
            X = scheduler()
            scheduler.run = X
            cat.coordinatingassistanttracker.basecat.zap()
        scheduler.run.waitForOne()
        scheduler.run.runThreads(slowmo=self.slowmo)
        background.lock.release()


if __name__ == '__main__':
    from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle
    import time
    background = background().start()
    MagnaDoodle().activate()
    while 1:
        time.sleep(1)
        print '.'