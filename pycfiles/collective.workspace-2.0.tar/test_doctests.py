# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/workflowed/tests/test_doctests.py
# Compiled at: 2008-07-25 18:15:12
from zope.testing import doctest
from unittest import TestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from plone.app.controlpanel.tests.cptc import ControlPanelTestCase
setupPloneSite()
OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def test_suite():
    tests = [
     'workflowed.txt']
    suite = TestSuite()
    for test in tests:
        suite.addTest(FunctionalDocFileSuite(test, optionflags=OPTIONFLAGS, package='collective.workflowed.tests', test_class=ControlPanelTestCase))

    return suite