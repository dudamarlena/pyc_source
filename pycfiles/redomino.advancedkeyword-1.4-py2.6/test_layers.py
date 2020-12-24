# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_layers.py
# Compiled at: 2013-05-08 04:41:18
from redomino.advancedkeyword.tests.base import FunctionalTestCase

class TestLayer(FunctionalTestCase):
    """ Test layers
    """

    def test_layer(self):
        """
        """
        from redomino.advancedkeyword.browser.interfaces import IRedominoAdvancedKeywordLayer
        from plone.browserlayer.utils import registered_layers
        self.assertTrue(IRedominoAdvancedKeywordLayer in registered_layers())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLayer))
    return suite