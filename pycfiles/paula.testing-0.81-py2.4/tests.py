# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paula/testing/tests.py
# Compiled at: 2008-08-14 09:21:53
"""
"""
import unittest
from paula.testing import get_test_suite, SuiteGenerator
from config import PACKAGE_NAME
sg = SuiteGenerator(PACKAGE_NAME)
tests = [
 sg.FunctionalDocFileSuite('README.txt')]
test_suite = get_test_suite(PACKAGE_NAME, tests)
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')