# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/tests/testDocTest.py
# Compiled at: 2007-09-08 18:44:19
from Products.PloneTestCase import PloneTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.Five.testbrowser import Browser
from simplon.plone.currency.tests import layer
import unittest
PloneTestCase.setupPloneSite()
from zope.testing import doctest
OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

class SimplonPloneCurrencyFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    __module__ = __name__
    layer = layer.SimplonPloneCurrency

    def getBrowser(self, loggedIn=False):
        """Utility method to get a, possibly logged-in, test browser."""
        browser = Browser()
        if loggedIn:
            browser.addHeader('Authorization', 'Basic %s:%s' % (PloneTestCase.default_user, PloneTestCase.default_password))
        return browser


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(FunctionalDocFileSuite('UserInterface.txt', optionflags=OPTIONFLAGS, test_class=SimplonPloneCurrencyFunctionalTestCase))
    return suite