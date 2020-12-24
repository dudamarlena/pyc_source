# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/recipe/cmd/tests/test_docs.py
# Compiled at: 2008-04-22 11:41:33
"""
Doctest runner for 'iw.recipe.cmd'.
"""
__docformat__ = 'restructuredtext'
import os, sys, unittest, zc.buildout.tests, zc.buildout.testing
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iw.recipe.cmd', test)
    test.globs['os'] = os
    test.globs['sys'] = sys
    test.globs['test_dir'] = os.path.dirname(__file__)


def test_suite():
    suite = unittest.TestSuite((doctest.DocFileSuite('../README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')