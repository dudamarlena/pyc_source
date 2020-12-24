# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/tests.py
# Compiled at: 2006-12-07 13:02:03
"""tests for shortcut package

$Id$
"""
import unittest, zope.testing.module
from zope.testing import doctest
from zope.app.testing import placelesssetup

def adaptersSetUp(test):
    zope.testing.module.setUp(test, name='zc.shortcut.adapters_test')
    placelesssetup.setUp(test)


def adaptersTearDown(test):
    zope.testing.module.tearDown(test, name='zc.shortcut.adapters_test')
    placelesssetup.tearDown(test)


def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('adapters.txt', setUp=adaptersSetUp, tearDown=adaptersTearDown, optionflags=doctest.ELLIPSIS), doctest.DocFileSuite('shortcut.txt', 'proxy.txt', 'adding.txt', 'factory.txt', setUp=placelesssetup.setUp, tearDown=placelesssetup.tearDown, optionflags=doctest.ELLIPSIS), doctest.DocTestSuite('zc.shortcut.constraints')))