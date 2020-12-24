# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/test/test_doctests.py
# Compiled at: 2008-11-09 13:28:02
from utils import buildDoctestSuite
modules = [
 'pylispng.lisp']
suite = buildDoctestSuite(modules)
if __name__ == '__main__':
    import unittest
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)