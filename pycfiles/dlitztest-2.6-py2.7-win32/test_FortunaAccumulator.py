# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Random\Fortuna\test_FortunaAccumulator.py
# Compiled at: 2013-03-13 13:15:35
"""Self-tests for Crypto.Random.Fortuna.FortunaAccumulator"""
__revision__ = '$Id$'
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
from Crypto.Util.py3compat import *
import unittest
from binascii import b2a_hex

class FortunaAccumulatorTests(unittest.TestCase):

    def setUp(self):
        global FortunaAccumulator
        from Crypto.Random.Fortuna import FortunaAccumulator

    def test_FortunaPool(self):
        """FortunaAccumulator.FortunaPool"""
        pool = FortunaAccumulator.FortunaPool()
        self.assertEqual(0, pool.length)
        self.assertEqual('5df6e0e2761359d30a8275058e299fcc0381534545f55cf43e41983f5d4c9456', pool.hexdigest())
        pool.append(b('abc'))
        self.assertEqual(3, pool.length)
        self.assertEqual('4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358', pool.hexdigest())
        pool.append(b('dbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'))
        self.assertEqual(56, pool.length)
        self.assertEqual(b('0cffe17f68954dac3a84fb1458bd5ec99209449749b2b308b7cb55812f9563af'), b2a_hex(pool.digest()))
        pool.reset()
        self.assertEqual(0, pool.length)
        pool.append(b('a') * 1000000)
        self.assertEqual(1000000, pool.length)
        self.assertEqual(b('80d1189477563e1b5206b2749f1afe4807e5705e8bd77887a60187a712156688'), b2a_hex(pool.digest()))

    def test_which_pools(self):
        """FortunaAccumulator.which_pools"""
        self.assertRaises(AssertionError, FortunaAccumulator.which_pools, 0)
        self.assertEqual(FortunaAccumulator.which_pools(1), [0])
        self.assertEqual(FortunaAccumulator.which_pools(2), [0, 1])
        self.assertEqual(FortunaAccumulator.which_pools(3), [0])
        self.assertEqual(FortunaAccumulator.which_pools(4), [0, 1, 2])
        self.assertEqual(FortunaAccumulator.which_pools(5), [0])
        self.assertEqual(FortunaAccumulator.which_pools(6), [0, 1])
        self.assertEqual(FortunaAccumulator.which_pools(7), [0])
        self.assertEqual(FortunaAccumulator.which_pools(8), [0, 1, 2, 3])
        for i in range(1, 32):
            self.assertEqual(FortunaAccumulator.which_pools(2 ** i - 1), [0])
            self.assertEqual(FortunaAccumulator.which_pools(2 ** i), range(i + 1))
            self.assertEqual(FortunaAccumulator.which_pools(2 ** i + 1), [0])

        self.assertEqual(FortunaAccumulator.which_pools(2147483648), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(4294967296), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(8589934592), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(17179869184), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(34359738368), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(68719476736), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(18446744073709551616), range(32))
        self.assertEqual(FortunaAccumulator.which_pools(340282366920938463463374607431768211456), range(32))

    def test_accumulator(self):
        """FortunaAccumulator.FortunaAccumulator"""
        fa = FortunaAccumulator.FortunaAccumulator()
        self.assertRaises(AssertionError, fa.random_data, 1)
        for p in range(32):
            fa.add_random_event(42, p, b('X') * 32)
            self.assertEqual(34, fa.pools[p].length)

        self.assertRaises(AssertionError, fa.random_data, 1)
        for p in range(32):
            fa.add_random_event(42, p, b('X') * 32)
            self.assertEqual(68, fa.pools[p].length)

        self.assertEqual('aef42a5dcbddab67e8efa118e1b47fde5d697f89beb971b99e6e8e5e89fbf064', fa.pools[0].hexdigest())
        self.assertEqual(None, fa.generator.key)
        self.assertEqual(0, fa.generator.counter.next_value())
        result = fa.random_data(32)
        self.assertEqual(b('b7b86bd9a27d96d7bb4add1b6b10d1572350b1c61253db2f8da233be726dc15f'), b2a_hex(result))
        self.assertEqual(b('f23ad749f33066ff53d307914fbf5b21da9667c7e86ba247655c9490e9d94a7c'), b2a_hex(fa.generator.key))
        self.assertEqual(5, fa.generator.counter.next_value())
        return

    def test_accumulator_pool_length(self):
        """FortunaAccumulator.FortunaAccumulator minimum pool length"""
        fa = FortunaAccumulator.FortunaAccumulator()
        self.assertEqual(fa.min_pool_size, 64)
        self.assertRaises(AssertionError, fa.random_data, 1)
        for i in range(15):
            for p in range(32):
                fa.add_random_event(2, p, b('XX'))
                self.assertRaises(AssertionError, fa.random_data, 1)

        fa.add_random_event(2, 0, b('XX'))
        fa.random_data(1)


def get_tests(config={}):
    from Crypto.SelfTest.st_common import list_test_cases
    return list_test_cases(FortunaAccumulatorTests)


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')