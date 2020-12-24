# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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