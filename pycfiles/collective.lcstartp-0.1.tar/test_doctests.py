# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/layout/authpersonalbar/tests/test_doctests.py
# Compiled at: 2011-04-07 05:20:15
import unittest2 as unittest, doctest
from plone.testing import layered
from collective.layout.authpersonalbar.tests._testing import COLLECTIVELAYOUTAUTHPERSONALBAR_INTEGRATION_TESTING, COLLECTIVELAYOUTAUTHPERSONALBAR_FUNCTIONAL_TESTING, optionflags
integration_tests = [
 'installation.txt']
functional_tests = [
 '../README.txt']

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([ layered(doctest.DocFileSuite('tests/%s' % file, package='collective.layout.authpersonalbar', optionflags=optionflags), layer=COLLECTIVELAYOUTAUTHPERSONALBAR_INTEGRATION_TESTING) for file in integration_tests
                   ])
    suite.addTests([ layered(doctest.DocFileSuite('tests/%s' % file, package='collective.layout.authpersonalbar', optionflags=optionflags), layer=COLLECTIVELAYOUTAUTHPERSONALBAR_FUNCTIONAL_TESTING) for file in functional_tests
                   ])
    return suite