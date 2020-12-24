# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/tests/test_utils.py
# Compiled at: 2008-10-10 10:13:58
"""
Testing utilities
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from iw.sitestat.tests.base import sitestatTestCase
from iw.sitestat import utils

class UtilsTestCase(sitestatTestCase):
    """We test utilities"""
    __module__ = __name__

    def testGetSite(self):
        site = utils.getSite()
        self.failUnless(site.getPhysicalPath() == self.portal.getPhysicalPath())

    def testValidateSitestatName(self):
        tests = [
         (
          'xxx', True), ('xx-x', True), ('xx_xx', True), ('xx%yy', False), (b'\xfexx', False), ('_xxx', False), ('xxx_', False), ('-xxx', False), ('xxx-', False)]
        for (label, valid) in tests:
            self.failUnlessEqual(utils.validateSitestatName(label), valid)

    def testSitestatifyTitle(self):
        tests = [
         ('Ascii', 'Ascii'), ('çon', 'con'), ('the clone', 'the-clone'), ('x<>&=y', 'x----y')]
        for (original, expected) in tests:
            got = utils.sitestatifyTitle(original, charset='utf-8')
            self.failUnlessEqual(got, expected)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(UtilsTestCase))
    return suite