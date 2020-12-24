# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bopen/recipe/libinc/tests.py
# Compiled at: 2007-10-14 04:05:50
import unittest, zc.buildout.tests, zc.buildout.testing
from zope.testing import doctest
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('bopen.recipe.libinc', test)


def test_suite():
    suite = unittest.TestSuite((doctest.DocFileSuite('README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')