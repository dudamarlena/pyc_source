# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/sk/recipe/xdv/tests.py
# Compiled at: 2010-05-29 17:42:53
from zope.testing import doctest, renormalizing
import unittest, zc.buildout.tests, zc.buildout.testing, re
_optionFlags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('lxml', test)
    zc.buildout.testing.install_develop('xdv', test)
    zc.buildout.testing.install_develop('sk.recipe.xdv', test)


def test_suite():
    suite = unittest.TestSuite((doctest.DocFileSuite('README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=_optionFlags, checker=renormalizing.RENormalizing([(re.compile('--prefix=\\S+sample-buildout'), '--prefix=/sample_buildout'), (re.compile('\\s/\\S+sample-buildout'), ' /sample_buildout'), zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')