# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/TaskKit/Tests/Test.py
# Compiled at: 2006-10-22 17:01:00
import os, sys
sys.path.insert(1, os.path.abspath('../..'))
import TaskKit, unittest

class TaskKitTest(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        from TaskKit.Scheduler import Scheduler
        self.scheduler = Scheduler()

    def checkBasics(self):
        sched = self.scheduler
        sched.start()

    def tearDown(self):
        self.scheduler.stop()
        self.scheduler = None
        return


def makeTestSuite():
    suite1 = unittest.makeSuite(TaskKitTest, 'check')
    return unittest.TestSuite((suite1,))


if __name__ == '__main__':
    runner = unittest.TextTestRunner(stream=sys.stdout)
    unittest.main(defaultTest='makeTestSuite', testRunner=runner)