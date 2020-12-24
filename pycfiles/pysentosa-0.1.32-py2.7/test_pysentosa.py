# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_pysentosa.py
# Compiled at: 2016-02-21 15:55:31
"""import os
import sys

TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,TOP_DIR)"""
import unittest, pysentosa.volatility as vo

def fun(x):
    return x + 1


class MyTest(unittest.TestCase):

    def test(self):
        self.assertEqual(fun(3), 4)