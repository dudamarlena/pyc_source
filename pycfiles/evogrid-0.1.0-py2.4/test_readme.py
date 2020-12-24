# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/tests/test_readme.py
# Compiled at: 2006-08-06 04:41:36
"""Test suite for the ``numeric`` package"""
import unittest
from zope.testing import doctest
import os
from evogrid.testing import OPTIONS

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocFileSuite(os.path.join('..', 'README.txt'), optionflags=OPTIONS))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')