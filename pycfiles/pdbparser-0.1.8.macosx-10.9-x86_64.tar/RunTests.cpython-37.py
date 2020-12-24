# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/UnitTests/RunTests.py
# Compiled at: 2019-02-16 11:54:31
# Size of source mod 2**32: 819 bytes
from __future__ import print_function
import unittest, sys, os
__TESTS_SUITE__ = unittest.TestSuite()
__RUNNER__ = unittest.TextTestRunner(verbosity=2)
path = os.path.join(os.getcwd().split('pdbparser')[0], 'pdbparser')
for all_test_suite in unittest.defaultTestLoader.discover('', pattern='Test*.py', top_level_dir=path):
    for test_suite in all_test_suite:
        __TESTS_SUITE__.addTests(test_suite)

def run_all_tests():
    __RUNNER__.run(__TESTS_SUITE__)


if __name__ == '__main__':
    import sys, os
    path = os.path.join(os.getcwd().split('pdbparser')[0], 'pdbparser')
    sys.path.insert(0, path)
    import pdbparser
    run_all_tests()