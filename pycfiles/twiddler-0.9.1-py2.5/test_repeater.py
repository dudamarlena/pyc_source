# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/test_repeater.py
# Compiled at: 2008-07-24 14:48:01
import unittest
from searchable import SearchableTests
from zope.interface.verify import verifyObject

class RepeaterTests(unittest.TestCase):

    def setUp(self):
        from twiddler import Twiddler
        self.r = Twiddler('<moo id="test"/>')['test'].repeater()

    def test_interface(self):
        from twiddler.interfaces import IRepeater
        verifyObject(IRepeater, self.r)


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(RepeaterTests),))