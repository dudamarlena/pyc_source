# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/z3c/recipe/staticlxml/tests/test_docs.py
# Compiled at: 2013-12-09 03:33:52
"""
Doctest runner for 'z3c.recipe.staticlxml'.
"""
__docformat__ = 'restructuredtext'
from zope.testing import renormalizing
import doctest, os, unittest, zc.buildout.testing, zc.buildout.tests, zc.recipe.cmmi.tests
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE
test_dir = os.path.dirname(os.path.abspath(__file__))

def setUp(test):
    zc.recipe.cmmi.tests.setUp(test)
    zc.buildout.testing.install_develop('z3c.recipe.staticlxml', test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('zc.recipe.cmmi', test)


def test_suite():
    suite = unittest.TestSuite((
     doctest.DocFileSuite('../README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, globs=dict(test_dir=test_dir), checker=renormalizing.RENormalizing([
      zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')