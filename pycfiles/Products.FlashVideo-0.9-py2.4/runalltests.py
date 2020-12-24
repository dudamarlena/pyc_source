# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\tests\runalltests.py
# Compiled at: 2009-01-27 14:30:52
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
import unittest
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