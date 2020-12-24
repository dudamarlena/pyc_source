# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/plone/recipe/cluster/tests/test_docs.py
# Compiled at: 2008-08-11 05:37:05
__doc__ = "\nDoctest runner for 'plone.recipe.cluster'.\n"
__docformat__ = 'restructuredtext'
import sys, unittest, zc.buildout.tests, zc.buildout.testing
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('plone.recipe.cluster', test)
    if sys.platform != 'win32':
        from plone.recipe.cluster import ctl
        ctl.DEBUG = True


def test_suite():
    if sys.platform == 'win32':
        doctest_file = '../README-win32.txt'
    else:
        doctest_file = '../README.txt'
    suite = unittest.TestSuite((doctest.DocFileSuite(doctest_file, setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')