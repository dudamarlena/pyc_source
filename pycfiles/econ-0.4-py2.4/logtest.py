# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/logtest.py
# Compiled at: 2007-04-18 06:57:54
import unittest, econ.log

class LogTest(unittest.TestCase):
    __module__ = __name__
    log = econ.log.get_logger()

    def testExists(self):
        self.failUnless(self.log, "Logger isn't there!")

    def testLogDebug(self):
        self.log.debug('Debug logging test. Please ignore this message.')

    def testLogInfo(self):
        self.log.info('Info logging test. Please ignore this message.')

    def testLogWarning(self):
        self.log.warning('Warning logging test. Please ignore this message.')

    def testLogError(self):
        self.log.error('Error logging test. Please ignore this message.')

    def testLogCritical(self):
        self.log.critical('Critical logging test. Please ignore this message.')