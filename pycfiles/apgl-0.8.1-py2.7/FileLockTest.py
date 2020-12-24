# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/FileLockTest.py
# Compiled at: 2011-12-24 06:33:22
import numpy, unittest, apgl
from apgl.util.FileLock import FileLock
from apgl.util.PathDefaults import PathDefaults

class FileLockTest(unittest.TestCase):

    def setUp(self):
        tempDir = PathDefaults.getTempDir()
        self.fileName = tempDir + 'abc'

    def testInit(self):
        fileLock = FileLock(self.fileName)

    def testLock(self):
        fileLock = FileLock(self.fileName)
        fileLock.lock()

    def testUnlock(self):
        fileLock = FileLock(self.fileName)
        fileLock.lock()
        self.assertTrue(fileLock.isLocked())
        fileLock.unlock()
        self.assertTrue(not fileLock.isLocked())