# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/recipe/subversion/tests/test_subversiondocs.py
# Compiled at: 2008-04-17 04:25:35
"""
Doctest runner for 'iw.recipe.subversion'.
"""
__docformat__ = 'restructuredtext'
import unittest, zc.buildout.tests, zc.buildout.testing
from shutil import copytree, rmtree
import os
from os.path import join
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
test_dir = os.path.split(__file__)[0]

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iw.recipe.subversion', test)
    repository = os.path.join(test_dir, 'test_repos')

    def create_repository():
        try:
            rmtree(repository)
        except:
            pass

        copytree(os.path.join(test_dir, 'repos'), repository)

    test.globs['create_repository'] = create_repository
    test.globs['repository'] = repository


def test_suite():
    suite = unittest.TestSuite((doctest.DocFileSuite('../README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, globs=globals(), optionflags=optionflags, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')