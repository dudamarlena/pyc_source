# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Box Sync/projects/2017/pinetree/tests/test_cpp.py
# Compiled at: 2018-01-26 16:22:56
# Size of source mod 2**32: 201 bytes
import unittest, subprocess

class MainTest(unittest.TestCase):

    def test_cpp(self):
        print('\n\nRunning C++ tests...\n')
        subprocess.call(['pinetree_test'])