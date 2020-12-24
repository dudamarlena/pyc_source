# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/tests/test_Readme.py
# Compiled at: 2008-05-06 03:12:20
import unittest
from zope.testing import doctest
import _base

def wrapper(test):
    _base.setUp(test)


def test_suite():
    d = dict(test_repo_path=_base.test_repo_path)
    return unittest.TestSuite((
     doctest.DocFileSuite('../readme.txt', setUp=wrapper, tearDown=_base.tearDown, globs=d, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')