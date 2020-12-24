# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/utils/test/test_registrator.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.utils.registrator}.
"""
import unittest
from spamfighter.utils.registrator import registrator

@registrator
def testRegistrator(cls):
    global testCls
    testCls = cls


class TestClass(object):
    testRegistrator()


class RegistratorTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.registrator.registrator}.
    """

    def test_Registrator(self):
        self.assertEquals(testCls, TestClass)