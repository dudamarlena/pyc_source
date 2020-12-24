# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_float.py
# Compiled at: 2019-06-26 11:58:00
import math
from unittest import TestCase
from pyutil import jsonutil as json

class TestFloat(TestCase):

    def test_floats(self):
        for num in [1617161771.765, math.pi, math.pi ** 100, math.pi ** (-100)]:
            self.assertEqual(float(json.dumps(num)), num)