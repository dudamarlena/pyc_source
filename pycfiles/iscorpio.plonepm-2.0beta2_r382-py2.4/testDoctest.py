# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/tests/testDoctest.py
# Compiled at: 2009-10-25 01:13:43
"""
The first step to use doctest for unit testing.
"""
import unittest, doctest
from Testing import ZopeTestCase
from base import PlonepmFunctionalTestCase
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

def test_suite():
    return unittest.TestSuite([ZopeTestCase.ZopeDocFileSuite('README.txt', package='iscorpio.plonepm', test_class=PlonepmFunctionalTestCase), ZopeTestCase.ZopeDocFileSuite('tests/README.txt', package='iscorpio.plonepm')])