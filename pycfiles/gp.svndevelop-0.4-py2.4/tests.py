# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/gp/svndevelop/tests.py
# Compiled at: 2008-02-05 15:50:59
"""
Generic Test case for gp.svndevelop doctest
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
from zope.testing import doctest, renormalizing
import zc.buildout.testing, svnhelper.testing, svnhelper.tests
from svnhelper.core import helper
test_package = os.path.dirname(svnhelper.tests.__file__)
test_package = os.path.join(test_package, 'tests', 'my.testing')

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('gp.svndevelop', test)
    svnhelper.testing.setUpRepository(test)
    test.globs['init_test_package'](test_package)
    helper.import_to(test.globs['package_dir'], test.globs['repository'])


def tearDown(test):
    svnhelper.testing.tearDownRepository(test)
    zc.buildout.testing.buildoutTearDown(test)


flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def test_suite():
    return unittest.TestSuite([doctest.DocFileSuite(os.path.join(os.path.dirname(__file__), 'README.txt'), optionflags=flags, globs=globals(), setUp=setUp, tearDown=tearDown, module_relative=False)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')