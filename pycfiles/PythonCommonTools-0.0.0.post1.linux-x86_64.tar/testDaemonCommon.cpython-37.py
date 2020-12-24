# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/test/daemonCommon/testDaemonCommon.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 4753 bytes
from unittest import TestCase
from time import sleep
from pythoncommontools.daemonCommon.daemonCommon import start, stop, status, Status, getPidFileName, Action, readPidFile
from test.daemonCommon.dummyDaemon import scriptName, scriptFullPath, statusFileFullPath
from os.path import isfile
from os import remove

class testDaemonCommon(TestCase):
    waitTime = 2
    pidFileName = getPidFileName(scriptName)

    def testProcessLifeCycle(self):
        """INFO : we test 2 commands :
         - tail -f /dev/null
         - top
         """
        for command in {'top', ('tail', '-f', '/dev/null')}:
            pid = start(command)
            self.assertGreater(pid, 0, 'correct process did not start')
            actualStatus = status(pid)
            self.assertIn(actualStatus, {Status.RUNNING.value, Status.SLEEPING.value, Status.ZOMBIE.value}, 'correct process status not as expected')
            stop(pid)
            sleep(testDaemonCommon.waitTime)

        actualStatus = status(pid)
        self.assertEqual(actualStatus, Status.ZOMBIE.value, 'stopped process status not as expected')
        stop(pid)
        pid = start('tail_')
        self.assertGreater(pid, 0, 'incorrect process did not start')
        sleep(testDaemonCommon.waitTime)
        actualStatus = status(pid)
        self.assertIn(actualStatus, {Status.ZOMBIE.value, Status.SLEEPING.value}, 'incorrect process status not as expected')
        stop(pid)
        sleep(testDaemonCommon.waitTime)
        for pid in {0, -1}:
            actualStatus = status(pid)
            self.assertIsNone(actualStatus, 'wrong PID process status not as expected')
            stop(pid)

    def testDaemonization(self):
        testDaemonCommon.cleanFiles()
        expectedPidsNumber = 2
        _ = 0
        pids = set()
        while _ < expectedPidsNumber:
            start('python3', scriptFullPath, Action.START.value)
            sleep(testDaemonCommon.waitTime)
            self.assertTrue(isfile(testDaemonCommon.pidFileName), 'PID file is not written')
            pid = readPidFile(scriptName)
            self.assertGreater(pid, 0, 'process did not start')
            pids.add(pid)
            _ += 1

        self.assertEqual(len(pids), expectedPidsNumber, 'PID number was not reset')
        start('python3', scriptFullPath, Action.STATUS.value)
        sleep(testDaemonCommon.waitTime)
        with open(statusFileFullPath, 'r') as (statusFile):
            status = statusFile.read()
        statusFile.closed
        self.assertEqual(status, Status.RUNNING.value, 'status is not ' + Status.RUNNING.value)
        _ = 0
        while _ < expectedPidsNumber:
            start('python3', scriptFullPath, Action.STOP.value)
            sleep(testDaemonCommon.waitTime)
            self.assertFalse(isfile(testDaemonCommon.pidFileName), 'PID file is not erased')
            _ += 1

        start('python3', scriptFullPath, Action.STATUS.value)
        sleep(testDaemonCommon.waitTime)
        with open(statusFileFullPath, 'r') as (statusFile):
            status = statusFile.read()
        statusFile.closed
        self.assertEqual(status, 'None', 'status is not erased')
        wrongDaemon = 'wrong.pypy'
        start('python3', wrongDaemon, Action.START.value)
        sleep(testDaemonCommon.waitTime)
        self.assertFalse(isfile(testDaemonCommon.pidFileName), 'PID file is written')
        start('python3', wrongDaemon, Action.STATUS.value)
        sleep(testDaemonCommon.waitTime)
        with open(statusFileFullPath, 'r') as (statusFile):
            status = statusFile.read()
        statusFile.closed
        self.assertEqual(status, 'None', 'status is ' + status)
        start('python3', wrongDaemon, Action.STOP.value)
        sleep(testDaemonCommon.waitTime)
        self.assertFalse(isfile(testDaemonCommon.pidFileName), 'PID file is created')
        testDaemonCommon.cleanFiles()

    @staticmethod
    def cleanFiles():
        if isfile(testDaemonCommon.pidFileName):
            remove(testDaemonCommon.pidFileName)
        if isfile(statusFileFullPath):
            remove(statusFileFullPath)