# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/TaskKit/Tests/BasicTest.py
# Compiled at: 2006-10-22 17:01:00
import os, sys
sys.path.insert(1, os.path.abspath('../..'))
import TaskKit
from TaskKit.Scheduler import Scheduler
from TaskKit.Task import Task
from time import time, sleep

class SimpleTask(Task):
    __module__ = __name__

    def run(self):
        if self.proceed():
            print self.name(), time()
        else:
            print 'Should not proceed', self.name()
            print 'proceed for %s=%s, isRunning=%s' % (self.name(), self.proceed(), self._handle._isRunning)


class LongTask(Task):
    __module__ = __name__

    def run(self):
        while 1:
            sleep(2)
            print 'proceed for %s=%s, isRunning=%s' % (self.name(), self.proceed(), self._handle._isRunning)
            if self.proceed():
                print '>>', self.name(), time()
            else:
                print 'Should not proceed:', self.name()
                return


def main():
    from time import localtime
    scheduler = Scheduler()
    scheduler.start()
    scheduler.addPeriodicAction(time(), 1, SimpleTask(), 'SimpleTask1')
    scheduler.addTimedAction(time() + 3, SimpleTask(), 'SimpleTask2')
    scheduler.addActionOnDemand(LongTask(), 'LongTask')
    scheduler.addDailyAction(localtime(time())[3], localtime(time())[4] + 1, SimpleTask(), 'DailyTask')
    sleep(5)
    print 'Demanding LongTask'
    scheduler.runTaskNow('LongTask')
    sleep(1)
    sleep(2)
    sleep(4)
    print 'Calling stop'
    scheduler.stop()
    print 'Test Complete'


if __name__ == '__main__':
    main()