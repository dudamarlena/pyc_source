# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/khh/khh_test.py
# Compiled at: 2017-11-27 21:02:42
# Size of source mod 2**32: 1164 bytes
from __future__ import print_function
import enum, unittest
from khh import KHeavyHitters
Dozen = 12
HalfDozen = Dozen / 2
BakersDozen = Dozen + 1
Bushel = 125

class Fruits(enum.Enum):
    Apple = 'apple'
    Orange = 'orange'
    Banana = 'banana'
    Strawberry = 'strawberry'
    Kiwi = 'kiwi'
    Mango = 'mango'


class KHeavyHittersTest(unittest.TestCase):
    __doc__ = '\n  Tests for KHeavyHitters\n  '

    def test_add(self):
        k = 5
        counts = dict()
        khh = KHeavyHitters(k)
        khh.add(Fruits.Banana)
        for i in range(Dozen):
            khh.add(Fruits.Apple)

        counts[Fruits.Apple] = i
        for i in range(Bushel * 2):
            khh.add(Fruits.Mango)

        counts[Fruits.Mango] = i
        for i in range(BakersDozen):
            khh.add(Fruits.Orange)

        counts[Fruits.Orange] = i
        for i in range(Bushel):
            khh.add(Fruits.Strawberry)

        counts[Fruits.Strawberry] = i
        top_k = khh.top_k()
        for f, v in counts.items():
            if v >= len(khh) / 5:
                self.assertTrue(f not in top_k)