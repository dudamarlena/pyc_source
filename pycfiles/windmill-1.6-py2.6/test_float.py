# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_float.py
# Compiled at: 2011-01-13 01:48:00
import math
from unittest import TestCase
import simplejson as json

class TestFloat(TestCase):

    def test_floats(self):
        for num in [1617161771.765, math.pi, math.pi ** 100, math.pi ** (-100), 3.1]:
            self.assertEquals(float(json.dumps(num)), num)
            self.assertEquals(json.loads(json.dumps(num)), num)

    def test_ints(self):
        for num in [1, 1, 4294967296, 18446744073709551616]:
            self.assertEquals(json.dumps(num), str(num))
            self.assertEquals(int(json.dumps(num)), num)