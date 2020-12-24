# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Util\test_number.py
# Compiled at: 2013-03-14 04:43:25
"""Self-tests for (some of) Crypto.Util.number"""
__revision__ = '$Id$'
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
import unittest

class MyError(Exception):
    """Dummy exception used for tests"""
    pass


class MiscTests(unittest.TestCase):

    def setUp(self):
        global math
        global number
        from Crypto.Util import number
        import math

    def test_ceil_shift(self):
        """Util.number.ceil_shift"""
        self.assertRaises(AssertionError, number.ceil_shift, -1, 1)
        self.assertRaises(AssertionError, number.ceil_shift, 1, -1)
        self.assertEqual(0, number.ceil_shift(0, 0))
        self.assertEqual(1, number.ceil_shift(1, 0))
        self.assertEqual(2, number.ceil_shift(2, 0))
        self.assertEqual(3, number.ceil_shift(3, 0))
        self.assertEqual(0, number.ceil_shift(0, 1))
        self.assertEqual(1, number.ceil_shift(1, 1))
        self.assertEqual(1, number.ceil_shift(2, 1))
        self.assertEqual(2, number.ceil_shift(3, 1))
        self.assertEqual(0, number.ceil_shift(0, 2))
        self.assertEqual(1, number.ceil_shift(1, 2))
        self.assertEqual(1, number.ceil_shift(2, 2))
        self.assertEqual(1, number.ceil_shift(3, 2))
        self.assertEqual(1, number.ceil_shift(4, 2))
        self.assertEqual(2, number.ceil_shift(5, 2))
        self.assertEqual(2, number.ceil_shift(6, 2))
        self.assertEqual(2, number.ceil_shift(7, 2))
        self.assertEqual(2, number.ceil_shift(8, 2))
        self.assertEqual(3, number.ceil_shift(9, 2))
        for b in range(3, 130, 3):
            self.assertEqual(0, number.ceil_shift(0, b))
            n = 1
            while n <= 2 ** (b + 2):
                q, r = divmod(n - 1, 2 ** b)
                expected = q + int(not not r)
                self.assertEqual((n - 1, b, expected), (
                 n - 1, b, number.ceil_shift(n - 1, b)))
                q, r = divmod(n, 2 ** b)
                expected = q + int(not not r)
                self.assertEqual((n, b, expected), (
                 n, b, number.ceil_shift(n, b)))
                q, r = divmod(n + 1, 2 ** b)
                expected = q + int(not not r)
                self.assertEqual((n + 1, b, expected), (
                 n + 1, b, number.ceil_shift(n + 1, b)))
                n *= 2

    def test_ceil_div(self):
        """Util.number.ceil_div"""
        self.assertRaises(TypeError, number.ceil_div, '1', 1)
        self.assertRaises(ZeroDivisionError, number.ceil_div, 1, 0)
        self.assertRaises(ZeroDivisionError, number.ceil_div, -1, 0)
        self.assertEqual(0, number.ceil_div(0, -1))
        self.assertEqual(-1, number.ceil_div(1, -1))
        self.assertEqual(-2, number.ceil_div(2, -1))
        self.assertEqual(-3, number.ceil_div(3, -1))
        self.assertEqual(0, number.ceil_div(0, 1))
        self.assertEqual(1, number.ceil_div(1, 1))
        self.assertEqual(2, number.ceil_div(2, 1))
        self.assertEqual(3, number.ceil_div(3, 1))
        self.assertEqual(0, number.ceil_div(0, 2))
        self.assertEqual(1, number.ceil_div(1, 2))
        self.assertEqual(1, number.ceil_div(2, 2))
        self.assertEqual(2, number.ceil_div(3, 2))
        self.assertEqual(2, number.ceil_div(4, 2))
        self.assertEqual(3, number.ceil_div(5, 2))
        self.assertEqual(0, number.ceil_div(0, 3))
        self.assertEqual(1, number.ceil_div(1, 3))
        self.assertEqual(1, number.ceil_div(2, 3))
        self.assertEqual(1, number.ceil_div(3, 3))
        self.assertEqual(2, number.ceil_div(4, 3))
        self.assertEqual(2, number.ceil_div(5, 3))
        self.assertEqual(2, number.ceil_div(6, 3))
        self.assertEqual(3, number.ceil_div(7, 3))
        self.assertEqual(0, number.ceil_div(0, 4))
        self.assertEqual(1, number.ceil_div(1, 4))
        self.assertEqual(1, number.ceil_div(2, 4))
        self.assertEqual(1, number.ceil_div(3, 4))
        self.assertEqual(1, number.ceil_div(4, 4))
        self.assertEqual(2, number.ceil_div(5, 4))
        self.assertEqual(2, number.ceil_div(6, 4))
        self.assertEqual(2, number.ceil_div(7, 4))
        self.assertEqual(2, number.ceil_div(8, 4))
        self.assertEqual(3, number.ceil_div(9, 4))
        self.assertEqual(3, number.ceil_div(-9, -4))
        self.assertEqual(2, number.ceil_div(-8, -4))
        self.assertEqual(2, number.ceil_div(-7, -4))
        self.assertEqual(2, number.ceil_div(-6, -4))
        self.assertEqual(2, number.ceil_div(-5, -4))
        self.assertEqual(1, number.ceil_div(-4, -4))
        self.assertEqual(1, number.ceil_div(-3, -4))
        self.assertEqual(1, number.ceil_div(-2, -4))
        self.assertEqual(1, number.ceil_div(-1, -4))
        self.assertEqual(0, number.ceil_div(0, -4))
        self.assertEqual(0, number.ceil_div(1, -4))
        self.assertEqual(0, number.ceil_div(2, -4))
        self.assertEqual(0, number.ceil_div(3, -4))
        self.assertEqual(-1, number.ceil_div(4, -4))
        self.assertEqual(-1, number.ceil_div(5, -4))
        self.assertEqual(-1, number.ceil_div(6, -4))
        self.assertEqual(-1, number.ceil_div(7, -4))
        self.assertEqual(-2, number.ceil_div(8, -4))
        self.assertEqual(-2, number.ceil_div(9, -4))

    def test_exact_log2(self):
        """Util.number.exact_log2"""
        self.assertRaises(TypeError, number.exact_log2, '0')
        self.assertRaises(ValueError, number.exact_log2, -1)
        self.assertRaises(ValueError, number.exact_log2, 0)
        self.assertEqual(0, number.exact_log2(1))
        self.assertEqual(1, number.exact_log2(2))
        self.assertRaises(ValueError, number.exact_log2, 3)
        self.assertEqual(2, number.exact_log2(4))
        self.assertRaises(ValueError, number.exact_log2, 5)
        self.assertRaises(ValueError, number.exact_log2, 6)
        self.assertRaises(ValueError, number.exact_log2, 7)
        e = 3
        n = 8
        while e < 16:
            if n == 2 ** e:
                self.assertEqual(e, number.exact_log2(n), 'expected=2**%d, n=%d' % (e, n))
                e += 1
            else:
                self.assertRaises(ValueError, number.exact_log2, n)
            n += 1

        for e in range(16, 65, 2):
            self.assertRaises(ValueError, number.exact_log2, 2 ** e - 1)
            self.assertEqual(e, number.exact_log2(2 ** e))
            self.assertRaises(ValueError, number.exact_log2, 2 ** e + 1)

    def test_exact_div(self):
        """Util.number.exact_div"""
        self.assertEqual(1, number.exact_div(1, 1))
        self.assertRaises(ValueError, number.exact_div, 1, 2)
        self.assertEqual(1, number.exact_div(2, 2))
        self.assertRaises(ValueError, number.exact_div, 3, 2)
        self.assertEqual(2, number.exact_div(4, 2))
        self.assertEqual(-1, number.exact_div(-1, 1))
        self.assertEqual(-1, number.exact_div(1, -1))
        self.assertRaises(ValueError, number.exact_div, -1, 2)
        self.assertEqual(1, number.exact_div(-2, -2))
        self.assertEqual(-2, number.exact_div(-4, 2))
        self.assertEqual(0, number.exact_div(0, 1))
        self.assertEqual(0, number.exact_div(0, 2))
        self.assertRaises(ZeroDivisionError, number.exact_div, 0, 0)
        self.assertRaises(ZeroDivisionError, number.exact_div, 1, 0)
        self.assertEqual(0, number.exact_div(0, 0, allow_divzero=True))
        self.assertRaises(ValueError, number.exact_div, 1, 0, allow_divzero=True)

    def test_floor_div(self):
        """Util.number.floor_div"""
        self.assertRaises(TypeError, number.floor_div, '1', 1)
        for a in range(-10, 10):
            for b in range(-10, 10):
                if b == 0:
                    self.assertRaises(ZeroDivisionError, number.floor_div, a, b)
                else:
                    self.assertEqual((a, b, int(math.floor(float(a) / b))), (
                     a, b, number.floor_div(a, b)))

    def test_getStrongPrime(self):
        """Util.number.getStrongPrime"""
        self.assertRaises(ValueError, number.getStrongPrime, 256)
        self.assertRaises(ValueError, number.getStrongPrime, 513)
        bits = 512
        x = number.getStrongPrime(bits)
        self.assertNotEqual(x % 2, 0)
        self.assertEqual(x > (1 << bits - 1) - 1, 1)
        self.assertEqual(x < 1 << bits, 1)
        e = 65537
        x = number.getStrongPrime(bits, e)
        self.assertEqual(number.GCD(x - 1, e), 1)
        self.assertNotEqual(x % 2, 0)
        self.assertEqual(x > (1 << bits - 1) - 1, 1)
        self.assertEqual(x < 1 << bits, 1)
        e = 65538
        x = number.getStrongPrime(bits, e)
        self.assertEqual(number.GCD(x - 1 >> 1, e), 1)
        self.assertNotEqual(x % 2, 0)
        self.assertEqual(x > (1 << bits - 1) - 1, 1)
        self.assertEqual(x < 1 << bits, 1)

    def test_isPrime(self):
        """Util.number.isPrime"""
        self.assertEqual(number.isPrime(-3), False)
        self.assertEqual(number.isPrime(-2), False)
        self.assertEqual(number.isPrime(1), False)
        self.assertEqual(number.isPrime(2), True)
        self.assertEqual(number.isPrime(3), True)
        self.assertEqual(number.isPrime(4), False)
        self.assertEqual(number.isPrime(10407932194664399081925240327364085538615262247266704805319112350403608059673360298012239441732324184842421613954281007791383566248323464908139906605677320762924129509389220345773183349661583550472959420547689811211693677147548478866962501384438260291732348885311160828538416585028255604666224831890918801847068222203140521026698435488732958028878050869736186900714720710555703168729087), True)
        self.assertEqual(number.isPrime(-10407932194664399081925240327364085538615262247266704805319112350403608059673360298012239441732324184842421613954281007791383566248323464908139906605677320762924129509389220345773183349661583550472959420547689811211693677147548478866962501384438260291732348885311160828538416585028255604666224831890918801847068222203140521026698435488732958028878050869736186900714720710555703168729087), False)
        for composite in (1152271, 1943521, 465658903,
         239626837621, 2028576353203, 25768686677581,
         47227901175703, 14910591535003,
         120175393101413203, 1858358298078962371,
         35051193821423205091, 4972725568723375711):
            self.assertEqual(number.isPrime(long(composite)), False)

    def test_size(self):
        self.assertEqual(number.size(2), 2)
        self.assertEqual(number.size(3), 2)
        self.assertEqual(number.size(162), 8)
        self.assertEqual(number.size(10664512), 24)
        self.assertEqual(number.size(114271173957383841654759309900399590453960166454672931570998620675636689540025513932023512771514410092510353526074687253816472581386512404723160802610417749684340444785376595696649176884149771730062910234452578113043294016308420031512280134131640653483544491686103567479056477782535675663257592116025533311397), 1024)


class FastmathTests(unittest.TestCase):

    def setUp(self):
        global number
        from Crypto.Util import number

    def test_negative_number_roundtrip_mpzToLongObj_longObjToMPZ(self):
        """Test that mpzToLongObj and longObjToMPZ (internal functions) roundtrip negative numbers correctly."""
        n = -100000000000000000000000000000000000
        e = 2
        k = number._fastmath.rsa_construct(n, e)
        self.assertEqual(n, k.n)
        self.assertEqual(e, k.e)

    def test_isPrime_randfunc_exception(self):
        """Test that when isPrime is called, an exception raised in randfunc is propagated."""

        def randfunc(n):
            raise MyError

        prime = 3536384141
        self.assertRaises(MyError, number._fastmath.isPrime, prime, randfunc=randfunc)

    def test_getStrongPrime_randfunc_exception(self):
        """Test that when getStrongPrime is called, an exception raised in randfunc is propagated."""

        def randfunc(n):
            raise MyError

        self.assertRaises(MyError, number._fastmath.getStrongPrime, 512, randfunc=randfunc)

    def test_isPrime_randfunc_bogus(self):
        """Test that when isPrime is called, an exception is raised if randfunc returns something bogus."""

        def randfunc(n):
            return

        prime = 3536384141
        self.assertRaises(TypeError, number._fastmath.isPrime, prime, randfunc=randfunc)

    def test_getStrongPrime_randfunc_bogus(self):
        """Test that when getStrongPrime is called, an exception is raised if randfunc returns something bogus."""

        def randfunc(n):
            return

        self.assertRaises(TypeError, number._fastmath.getStrongPrime, 512, randfunc=randfunc)


def get_tests(config={}):
    from Crypto.SelfTest.st_common import list_test_cases
    tests = list_test_cases(MiscTests)
    try:
        from Crypto.PublicKey import _fastmath
        tests += list_test_cases(FastmathTests)
    except ImportError:
        from distutils.sysconfig import get_config_var
        import inspect, os.path
        _fm_path = os.path.normpath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../../PublicKey/_fastmath' + get_config_var('SO'))
        if os.path.exists(_fm_path):
            raise ImportError('While the _fastmath module exists, importing ' + 'it failed. This may point to the gmp or mpir shared library ' + 'not being in the path. _fastmath was found at ' + _fm_path)

    return tests


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')