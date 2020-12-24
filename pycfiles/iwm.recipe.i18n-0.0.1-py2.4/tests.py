# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iwm/recipe/i18n/tests.py
# Compiled at: 2007-08-29 09:00:32
import re, zc.buildout.testing, unittest, zope.testing
from zope.testing import doctest, renormalizing

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iwm.recipe.i18n', test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('zope.testing', test)


def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path, zc.buildout.testing.normalize_script, zc.buildout.testing.normalize_egg_py, (re.compile('#!\\S+python\\S*'), '#!python'), (re.compile('\\d[.]\\d+ seconds'), '0.001 seconds'), (re.compile('zope.testing-[^-]+-'), 'zope.testing-X-'), (re.compile('setuptools-[^-]+-'), 'setuptools-X-')])),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')