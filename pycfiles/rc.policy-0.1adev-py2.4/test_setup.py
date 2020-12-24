# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rc/policy/tests/test_setup.py
# Compiled at: 2009-05-28 09:52:17
import unittest
from rc.policy.tests.base import RcPolicyTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(RcPolicyTestCase):
    __module__ = __name__

    def test_portal_title(self):
        self.assertEquals('Redaktionskomponente des SFB 600', self.portal.getProperty('title'))

    def test_portal_description(self):
        self.assertEquals('Evaluationsumgebung', self.portal.getProperty('description'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite