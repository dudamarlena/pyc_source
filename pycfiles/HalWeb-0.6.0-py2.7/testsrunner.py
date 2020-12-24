# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/tests/testsrunner.py
# Compiled at: 2011-12-25 05:31:43
import sys, os
from os.path import dirname, join
halWebImport = join(dirname(dirname(os.path.abspath(__file__))), 'lib')
print '===================='
print 'importing halWeb'
print '\t', halWebImport
print '===================='
sys.path.append(halWebImport)
import test_imports
sys.modules['imports'] = test_imports
globals()['imports'] = test_imports
locals()['imports'] = test_imports
import unittest, codeBlockHelperTests, BlockTestCases, BlockLocatorTestCases, packagerTestCases, sys
if __name__ == '__main__':
    loader = unittest.TestLoader()
    ltm = loader.loadTestsFromModule
    runner = unittest.TextTestRunner(stream=sys.stdout, descriptions=3, verbosity=3)
    all = unittest.TestSuite([
     ltm(BlockTestCases),
     ltm(codeBlockHelperTests),
     ltm(BlockLocatorTestCases),
     ltm(packagerTestCases)])
    runner.run(all)