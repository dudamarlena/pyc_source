# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyWhatCounts/tests/runalltests.py
# Compiled at: 2009-05-13 06:43:53
import os, sys, unittest
TestRunner = unittest.TextTestRunner
suite = unittest.TestSuite()
tests = os.listdir(os.curdir)
tests = [ n[:-3] for n in tests if n.startswith('test') if n.endswith('.py') ]
for test in tests:
    m = __import__(test)
    if hasattr(m, 'test_suite'):
        suite.addTest(m.test_suite())

if __name__ == '__main__':
    TestRunner().run(suite)