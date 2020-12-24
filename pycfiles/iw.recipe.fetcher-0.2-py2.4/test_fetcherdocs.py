# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/recipe/fetcher/tests/test_fetcherdocs.py
# Compiled at: 2008-01-11 04:41:24
"""
Generic Test case for 'iw.recipe.fetcher' doctest
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
from os.path import isdir, join
from shutil import rmtree, copytree
from zope.testing import doctest, renormalizing
import zc.buildout.testing

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iw.recipe.fetcher', test)


tearDown = zc.buildout.testing.buildoutTearDown
current_dir = os.path.dirname(__file__)

def doc_suite(test_dir, setUp=setUp, tearDown=tearDown, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()
    globs['test_dir'] = current_dir
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    docs = []
    for dir_ in ('doctests', 'docs'):
        doctest_dir = os.path.join(package_dir, dir_)
        docs.extend([ os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt') ])

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, globs=globs, setUp=setUp, tearDown=tearDown, module_relative=False))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')