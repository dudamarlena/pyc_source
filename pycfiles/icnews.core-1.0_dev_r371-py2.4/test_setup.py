# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/core/tests/test_setup.py
# Compiled at: 2008-10-06 10:31:17
"""Test icNews.Core setup on installation.
"""
import unittest
from base import icNewsCoreTestCase
from icnews.core.interfaces import IicNewsSite

class TestICNewsCoreSetup(icNewsCoreTestCase):
    """Testing the product setup"""
    __module__ = __name__

    def afterSetUp(self):
        """Ran before every unit test"""
        self.qi = self.portal.portal_quickinstaller

    def test_install(self):
        self.failUnless(self.qi.isProductInstalled('icnews.core'))

    def test_site_provides(self):
        self.failUnless(IicNewsSite.providedBy(self.portal))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestICNewsCoreSetup))
    return suite