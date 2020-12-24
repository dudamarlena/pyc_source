# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_portal.py
# Compiled at: 2013-05-08 04:41:18
from redomino.advancedkeyword.tests.base import TestCase

class TestPortal(TestCase):
    """ Check if js, css, etc are correctly registered
    """

    def test_js(self):
        """ dynatree plugin"""
        portal_javascripts = self.portal.portal_javascripts
        resource_ids = [ item.getId() for item in portal_javascripts.resources ]
        self.assertTrue('++resource++redomino.advancedkeyword.resources/jquery.keywordtree.js' in resource_ids)
        self.assertTrue('++resource++redomino.advancedkeyword.resources/subjectkeywordtree.js' in resource_ids)

    def test_css(self):
        """ Css resources loaded? """
        portal_css = self.portal.portal_css
        resource_ids = [ item.getId() for item in portal_css.resources ]
        self.assertTrue('++resource++redomino.advancedkeyword.resources/jquery.keywordtree.css' in resource_ids)

    def test_actions(self):
        """ Test portal actions """
        portal_actions = self.portal.portal_actions
        self.assertTrue('keywords' in [ item['id'] for item in portal_actions.listActionInfos() ])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortal))
    return suite