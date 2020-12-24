# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/mptt/tests/tests.py
# Compiled at: 2009-10-31 23:19:40
import doctest, unittest
from mptt.tests import doctests
from mptt.tests import testcases

def suite():
    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(doctests))
    s.addTest(unittest.defaultTestLoader.loadTestsFromModule(testcases))
    return s