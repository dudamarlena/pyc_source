# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/control/ops_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1421 bytes
import unittest
from bibliopixel.control.ops import Ops, OPS

class OpsTest(unittest.TestCase):

    def test_empty(self):
        ops = Ops()
        self.assertEqual(ops(0), 0)
        self.assertEqual(ops(1), 1)

    def test_single(self):
        ops = Ops('sqrt')
        self.assertEqual(ops(0), 0)
        self.assertEqual(ops(1), 1)
        self.assertAlmostEqual(ops(2) * ops(2), 2)

    def test_two(self):
        ops = Ops('mul', 2)
        self.assertEqual(ops(0), 0)
        self.assertEqual(ops(1), 2)
        ops = Ops('div', 2)
        self.assertEqual(ops(0), 0)
        self.assertEqual(ops(2), 1)
        ops = Ops('rdiv', 10)
        self.assertEqual(ops(2), 5)
        self.assertEqual(ops(10), 1)

    def test_multi(self):
        ops = Ops('mul', 2, 'sub', 4, 'sqrt')
        self.assertEqual(ops(2), 0)
        self.assertEqual(ops(10), 4)

    def test_all(self):
        for k, v in OPS[0].items():
            v(0.5 if k == 'atanh' else 1)

        for v in OPS[1].values():
            v(1, 1)

    def test_error(self):

        def raisesOps(*s):
            with self.assertRaises(Exception) as (e):
                Ops(*s)
            return e

        Ops()
        raisesOps(0)
        raisesOps('unknown')
        raisesOps('mul')
        Ops('sqrt')
        raisesOps('sqrt', 2)
        raisesOps('sqrt', 'mul')
        Ops('sqrt', 'mul', 2)
        raisesOps('sqrt', 'mul', 2, 3)