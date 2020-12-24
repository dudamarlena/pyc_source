# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/exceptions_test.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 340 bytes
from domain import exceptions
import unittest

class ExceptionsTest(unittest.TestCase):
    repo = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exceptions(self):
        nf = exceptions.NotFoundException('record not found : aaa')
        print(nf)
        self.assertEqual(nf.err_code, 1001)