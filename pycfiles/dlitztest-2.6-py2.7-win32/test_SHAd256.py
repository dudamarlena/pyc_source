# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Random\Fortuna\test_SHAd256.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Random.Fortuna.SHAd256"""
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('5df6e0e2761359d30a8275058e299fcc0381534545f55cf43e41983f5d4c9456', '', "'' (empty string)"),
 ('4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358', 'abc'),
 ('0cffe17f68954dac3a84fb1458bd5ec99209449749b2b308b7cb55812f9563af', 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')]

def get_tests(config={}):
    from Crypto.Random.Fortuna import SHAd256
    from Crypto.SelfTest.Hash.common import make_hash_tests
    return make_hash_tests(SHAd256, 'SHAd256', test_data, 32)


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')