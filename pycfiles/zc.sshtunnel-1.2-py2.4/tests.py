# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zc/sshtunnel/tests.py
# Compiled at: 2007-03-28 20:00:10
"""Test harness for zc.sshtunnel.

"""
__docformat__ = 'reStructuredText'
import unittest
from zope.testing import doctest
from zope.testing import renormalizing
import zc.buildout.testing

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('zc.sshtunnel', test)
    zc.buildout.testing.install('zope.testing', test)


def test_suite():
    return unittest.TestSuite([doctest.DocFileSuite('README.txt', setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown, optionflags=doctest.ELLIPSIS, checker=renormalizing.RENormalizing([zc.buildout.testing.normalize_path]))])