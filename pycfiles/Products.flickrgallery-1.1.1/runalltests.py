# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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