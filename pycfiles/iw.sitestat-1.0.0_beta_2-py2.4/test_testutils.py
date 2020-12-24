# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/tests/test_testutils.py
# Compiled at: 2008-10-10 10:13:58
"""
Testing... the test framework
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from iw.sitestat.tests.base import sitestatTestCase
from iw.sitestat.tests import utils as in_utils
from iw.sitestat.config import HAVE_COLLAGE, HAVE_PLONEARTICLE, HAVE_SIMPLEALIAS

class UtilsTestCase(sitestatTestCase):
    """We test utilities for testcases"""
    __module__ = __name__

    def testTestRequest(self):
        request = in_utils.TestRequest()
        request.set('dummy', 'stuff')
        self.failUnlessEqual(request.get('dummy'), 'stuff')

    def testAddFile(self):
        self.loginAsPortalOwner()
        foo_file = in_utils.addFile(self.portal, 'foo', 'Foo')
        self.failUnlessEqual(foo_file.title_or_id(), 'Foo')

    def testAddCollage(self):
        if HAVE_COLLAGE:
            self.loginAsPortalOwner()
            foo_collage = in_utils.addCollage(self.portal, 'col', 'Collage')
            self.failUnlessEqual(foo_collage.title_or_id(), 'Collage')

    def testAddPloneArticle(self):
        if HAVE_PLONEARTICLE:
            self.loginAsPortalOwner()
            foo_article = in_utils.addPloneArticle(self.portal, 'art', 'Article')
            self.failUnlessEqual(foo_article.title_or_id(), 'Article')

    def testAddSimpleAlias(self):
        if HAVE_SIMPLEALIAS:
            self.loginAsPortalOwner()
            foo_alias = in_utils.addSimpleAlias(self.portal, 'alias', 'Alias')
            self.failUnlessEqual(foo_alias.title_or_id(), 'Alias not set')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(UtilsTestCase))
    return suite