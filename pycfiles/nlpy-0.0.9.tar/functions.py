# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/test/deep/functions.py
# Compiled at: 2014-11-14 01:11:16
import unittest
from nlpy.deep.functions import VarMap

class FunctionsTest(unittest.TestCase):

    def test_varmap(self):
        vars = VarMap()
        vars.x = 1
        print vars.x
        print vars.y