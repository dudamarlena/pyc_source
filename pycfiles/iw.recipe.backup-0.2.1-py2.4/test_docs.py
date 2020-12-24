# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/recipe/backup/tests/test_docs.py
# Compiled at: 2009-11-25 08:12:06
"""
Doctest runner for 'iw.recipe.backup'.
"""
__docformat__ = 'restructuredtext'
import os, re, unittest, zc.buildout.tests, zc.buildout.testing
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
test_dir = os.path.dirname(__file__)

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iw.recipe.backup', test)


def tearDown(test):
    from iw.recipe.backup import testing
    testing.remove_input()
    zc.buildout.testing.buildoutTearDown(test)


def test_suite():
    suite = unittest.TestSuite((doctest.DocFileSuite('../README.txt', setUp=setUp, tearDown=tearDown, optionflags=optionflags, globs=globals(), checker=renormalizing.RENormalizing([(re.compile('-[0-9]{4}'), '-XXXX'), (re.compile('-[0-9]{2}'), '-XX'), zc.buildout.testing.normalize_path])),))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')