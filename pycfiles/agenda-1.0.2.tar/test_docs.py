# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/ageliaco/recipe/csvconfig/tests/test_docs.py
# Compiled at: 2015-08-03 05:45:54
__doc__ = "\nDoctest runner for 'ageliaco.recipe.csvconfig'.\n"
__docformat__ = 'restructuredtext'
import unittest, zc.buildout.tests, zc.buildout.testing
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('ageliaco.recipe.csvconfig', test)


def test_suite():
    suite = unittest.TestSuite((
     doctest.DocFileSuite('../README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, checker=renormalizing.RENormalizing([
      zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')