# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/tests/test_doctests.py
# Compiled at: 2013-10-15 10:29:21
import unittest2 as unittest, doctest
from plone.testing import layered
from plone.multilingual.testing import PLONEMULTILINGUAL_INTEGRATION_TESTING, PLONEMULTILINGUAL_FUNCTIONAL_TESTING, optionflags
integration_tests = [
 '../../../README.rst']
functional_tests = []

def test_suite():
    return unittest.TestSuite([ layered(doctest.DocFileSuite('%s' % f, package='plone.multilingual', optionflags=optionflags), layer=PLONEMULTILINGUAL_INTEGRATION_TESTING) for f in integration_tests
                              ] + [ layered(doctest.DocFileSuite('%s' % f, package='plone.multilingual', optionflags=optionflags), layer=PLONEMULTILINGUAL_FUNCTIONAL_TESTING) for f in functional_tests
                                  ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')