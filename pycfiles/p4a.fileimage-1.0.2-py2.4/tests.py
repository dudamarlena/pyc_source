# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/fileimage/tests.py
# Compiled at: 2007-11-30 08:40:44
import unittest
from zope.testing import doctest
from zope.component import testing

def test_suite():
    return unittest.TestSuite((doctest.DocTestSuite('p4a.fileimage._property'), doctest.DocFileSuite('file.txt', setUp=testing.setUp, tearDown=testing.tearDown)))