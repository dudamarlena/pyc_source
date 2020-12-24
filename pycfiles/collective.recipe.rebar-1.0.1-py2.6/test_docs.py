# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/recipe/rebar/tests/test_docs.py
# Compiled at: 2010-03-09 09:03:58
"""
Doctest runner for 'collective.recipe.rebar'.
"""
__docformat__ = 'restructuredtext'
import unittest, zc.buildout.tests, zc.buildout.testing
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('collective.recipe.rebar', test)


def test_suite():
    suite = unittest.TestSuite((
     doctest.DocFileSuite('../README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, checker=renormalizing.RENormalizing([
      zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')