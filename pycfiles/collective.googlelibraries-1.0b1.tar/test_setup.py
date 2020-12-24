# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/toutpt/workspace/collective.googlelibraries/collective/googlelibraries/tests/test_setup.py
# Compiled at: 2010-11-27 09:10:51
import unittest
from collective.googlelibraries.tests import base

class TestSetup(base.TestCase):

    def test_layer(self):
        self.failUnless(1 == 1)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite