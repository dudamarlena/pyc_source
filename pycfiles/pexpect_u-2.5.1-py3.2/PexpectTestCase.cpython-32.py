# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/PexpectTestCase.py
# Compiled at: 2011-11-02 15:34:09
import unittest, sys, os

class PexpectTestCase(unittest.TestCase):

    def setUp(self):
        self.PYTHONBIN = sys.executable
        self.original_path = os.getcwd()
        newpath = os.path.dirname(__file__)
        os.chdir(newpath)
        print('\n', self.id(), end=' ')
        unittest.TestCase.setUp(self)

    def tearDown(self):
        os.chdir(self.original_path)