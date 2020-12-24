# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Box Sync/projects/2018/pinetree/tests/cpp_test.py
# Compiled at: 2018-02-16 15:22:24
# Size of source mod 2**32: 366 bytes
import unittest, subprocess, os

class MainTest(unittest.TestCase):

    def test_cpp(self):
        print('\n\nTesting C++ code...')
        subprocess.check_call(os.path.join(os.path.dirname(os.path.relpath(__file__)), 'bin', 'pinetree_test'))
        print('\nResuming Python tests...\n')


if __name__ == '__main__':
    unittest.main()