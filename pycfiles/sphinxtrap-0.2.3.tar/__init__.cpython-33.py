# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jose/Documents/projects/sphinxtrap/repo/tests/__init__.py
# Compiled at: 2014-02-15 15:04:40
# Size of source mod 2**32: 349 bytes
import sys, os
from .mocking import unittest, TestSphinxtrap
from .builder import BuildProject

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSphinxtrap))
    suite.addTests(unittest.makeSuite(BuildProject))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())