# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iwm/recipe/bebopinstance/tests.py
# Compiled at: 2007-07-16 10:35:40
import os, re, shutil, sys, tempfile, pkg_resources, zc.buildout.testing, unittest, zope.testing
from zope.testing import doctest, renormalizing

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('zc.recipe.zope3instance', test)
    zc.buildout.testing.install('zope.testing', test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    sample_zope3 = test.globs['tmpdir']()
    test.globs['sample_zope3'] = sample_zope3
    test.globs['mkdir'](sample_zope3, 'zopeskel')
    test.globs['mkdir'](sample_zope3, 'zopeskel', 'etc')
    test.globs['write'](sample_zope3, 'zopeskel', 'etc', 'ftesting.zcml', 'This is ftesting')
    test.globs['write'](sample_zope3, 'zopeskel', 'etc', 'site.zcml', 'This is site')
    test.globs['mkdir'](sample_zope3, 'zopeskel', 'package-includes')


def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, checker=renormalizing.RENormalizing([])),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')