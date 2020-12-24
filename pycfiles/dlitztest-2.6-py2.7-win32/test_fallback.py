# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Random\OSRNG\test_fallback.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Random.OSRNG.fallback"""
__revision__ = '$Id$'
import unittest

class SimpleTest(unittest.TestCase):

    def runTest(self):
        """Crypto.Random.OSRNG.fallback.new()"""
        import Crypto.Random.OSRNG.fallback
        randobj = Crypto.Random.OSRNG.fallback.new()
        x = randobj.read(16)
        y = randobj.read(16)
        self.assertNotEqual(x, y)


def get_tests(config={}):
    return [
     SimpleTest()]


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')