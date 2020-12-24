# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/tests.py
# Compiled at: 2009-09-20 13:59:59
import unittest, doctest
if __name__ == '__main__':
    suite = doctest.DocFileSuite('README.txt')
    runner = unittest.TextTestRunner()
    runner.run(suite)