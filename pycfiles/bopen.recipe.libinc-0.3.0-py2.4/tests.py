# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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