# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc_tests/test_singleton.py
# Compiled at: 2018-07-31 10:42:31
import unittest
from summerrpc.transport import RecordTransport

class TestSingleton(unittest.TestCase):

    def testRecordTransport(self):
        rt1 = RecordTransport()
        rt2 = RecordTransport()
        self.assertTrue(rt1 is rt2)