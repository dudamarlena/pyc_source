# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zc/creditcard/tests.py
# Compiled at: 2007-11-14 09:09:03
"""Tests for zc.ssl

$Id: tests.py 81834 2007-11-14 13:55:52Z alga $
"""
import unittest, zope.testing.doctest

def test_suite():
    suite = unittest.TestSuite([zope.testing.doctest.DocTestSuite('zc.creditcard')])
    return suite