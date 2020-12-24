# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_keywordmap.py
# Compiled at: 2013-05-08 04:41:18
from zope.component import getMultiAdapter
from redomino.advancedkeyword.tests.base import TestCase

class TestKeywordmap(TestCase):
    """
    """

    def afterSetUp(self):
        super(TestKeywordmap, self).afterSetUp()
        self.sitemap = getMultiAdapter((self.portal, self.portal.REQUEST), name='keywordsmap')

    def test_enabled_disabled_view(self):
        """ Test keywordmapenabled view. This view is used by the 'Keywords map' action """
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = True
        self.assertTrue(self.portal.restrictedTraverse('keywordmapenabled')())
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = False
        self.assertFalse(self.portal.restrictedTraverse('keywordmapenabled')())

    def test_enabled(self):
        """
        If the keyword map sitemap is disabled throws a 404 error.
        """
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = True
        self.sitemap()
        self.assertTrue('Subjects map' in self.portal())

    def test_disabled(self):
        """
        If the keyword map sitemap is disabled throws a 404 error.
        """
        from zope.publisher.interfaces import INotFound
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = False
        self.assertFalse('Subjects map' in self.portal())
        try:
            self.sitemap()
        except Exception, e:
            self.assertTrue(INotFound.providedBy(e))
        else:
            self.fail('The disabled sitemap view has to raise NotFound!')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestKeywordmap))
    return suite