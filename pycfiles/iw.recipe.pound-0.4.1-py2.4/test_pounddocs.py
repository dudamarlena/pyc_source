# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/recipe/pound/tests/test_pounddocs.py
# Compiled at: 2008-07-02 13:21:38
"""
Generic Test case for 'iw.recipe.pound' doctest
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os, zc.buildout.testing
from zope.testing import doctest, renormalizing
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
current_dir = os.path.dirname(__file__)
import urllib2

def urlopen(url):
    return open(os.path.join(current_dir, 'Pound-2.3.2.tgz'))


urllib2.urlopen = urlopen

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iw.recipe.pound', test)
    zc.buildout.testing.install_develop('zc.recipe.cmmi', test)


def test_suite():
    globs = globals()
    globs['test_dir'] = current_dir
    globs['bin_dir'] = '%s/bin' % current_dir
    suite = unittest.TestSuite((doctest.DocFileSuite('../docs/building.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, globs=globs, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path])), doctest.DocFileSuite('../docs/configuring.txt', setUp=setUp, globs=globs, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path])), doctest.DocFileSuite('../docs/technical.txt', setUp=setUp, globs=globs, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=optionflags, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path]))))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')