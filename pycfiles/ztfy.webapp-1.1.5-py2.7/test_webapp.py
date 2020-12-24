# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/webapp/webapp_base/tests/test_webapp.py
# Compiled at: 2011-12-19 03:06:16
import re, doctest, zc.buildout.testing
from zope.testing import renormalizing

def easy_install_SetUp(test):
    zc.buildout.testing.buildoutSetUp(test)


def test_suite():
    return doctest.DocFileSuite('webapp.txt', setUp=easy_install_SetUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE, checker=renormalizing.RENormalizing([
     zc.buildout.testing.normalize_endings,
     zc.buildout.testing.normalize_script,
     zc.buildout.testing.normalize_egg_py,
     (
      re.compile('Running .*python.* setup.py'), 'Running python setup.py'),
     (
      re.compile('\\\\'), '/')]))