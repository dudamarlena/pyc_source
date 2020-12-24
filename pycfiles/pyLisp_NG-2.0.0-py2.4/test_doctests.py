# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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