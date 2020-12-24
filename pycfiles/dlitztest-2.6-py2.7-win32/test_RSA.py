# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\PublicKey\test_RSA.py
# Compiled at: 2013-03-14 04:43:25
"""Self-test suite for Crypto.PublicKey.RSA"""
__revision__ = '$Id$'
import sys, os, pickle
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
from Crypto.Util.py3compat import *
import unittest
from Crypto.SelfTest.st_common import list_test_cases, a2b_hex, b2a_hex

class RSATest(unittest.TestCase):
    plaintext = '\n           eb 7a 19 ac e9 e3 00 63 50 e3 29 50 4b 45 e2\n        ca 82 31 0b 26 dc d8 7d 5c 68 f1 ee a8 f5 52 67\n        c3 1b 2e 8b b4 25 1f 84 d7 e0 b2 c0 46 26 f5 af\n        f9 3e dc fb 25 c9 c2 b3 ff 8a e1 0e 83 9a 2d db\n        4c dc fe 4f f4 77 28 b4 a1 b7 c1 36 2b aa d2 9a\n        b4 8d 28 69 d5 02 41 21 43 58 11 59 1b e3 92 f9\n        82 fb 3e 87 d0 95 ae b4 04 48 db 97 2f 3a c1 4f\n        7b c2 75 19 52 81 ce 32 d2 f1 b7 6d 4d 35 3e 2d\n    '
    ciphertext = '\n        12 53 e0 4d c0 a5 39 7b b4 4a 7a b8 7e 9b f2 a0\n        39 a3 3d 1e 99 6f c8 2a 94 cc d3 00 74 c9 5d f7\n        63 72 20 17 06 9e 52 68 da 5d 1c 0b 4f 87 2c f6\n        53 c1 1d f8 23 14 a6 79 68 df ea e2 8d ef 04 bb\n        6d 84 b1 c3 1d 65 4a 19 70 e5 78 3b d6 eb 96 a0\n        24 c2 ca 2f 4a 90 fe 9f 2e f5 c9 c1 40 e5 bb 48\n        da 95 36 ad 87 00 c8 4f c9 13 0a de a7 4e 55 8d\n        51 a7 4d df 85 d8 b5 0d e9 68 38 d6 06 3e 09 55\n    '
    modulus = '\n        bb f8 2f 09 06 82 ce 9c 23 38 ac 2b 9d a8 71 f7\n        36 8d 07 ee d4 10 43 a4 40 d6 b6 f0 74 54 f5 1f\n        b8 df ba af 03 5c 02 ab 61 ea 48 ce eb 6f cd 48\n        76 ed 52 0d 60 e1 ec 46 19 71 9d 8a 5b 8b 80 7f\n        af b8 e0 a3 df c7 37 72 3e e6 b4 b7 d9 3a 25 84\n        ee 6a 64 9d 06 09 53 74 88 34 b2 45 45 98 39 4e\n        e0 aa b1 2d 7b 61 a5 1f 52 7a 9a 41 f6 c1 68 7f\n        e2 53 72 98 ca 2a 8f 59 46 f8 e5 fd 09 1d bd cb\n    '
    e = 17
    prime_factor = '\n        c9 7f b1 f0 27 f4 53 f6 34 12 33 ea aa d1 d9 35\n        3f 6c 42 d0 88 66 b1 d0 5a 0f 20 35 02 8b 9d 86\n        98 40 b4 16 66 b4 2e 92 ea 0d a3 b4 32 04 b5 cf\n        ce 33 52 52 4d 04 16 a5 a4 41 e7 00 af 46 15 03\n    '
    pickled_key_2_3 = "(iCrypto.PublicKey.RSA\n_RSAobj\np0\n(dp2\nS'e'\np3\nL17L\nsS'd'\np4\nL116467631542930861601478893145535067646063536882841491209835874887938222956830669640652587163148071314937674955822237189053368758722351580531956820574156366843733156436163097164007967904900300775223658035432332923992450647439719694734683045367149790102198810033962358618370829441895425705728523874962107052993L\nsS'n'\np5\nL131996649081988309815009412231606409998872008467220356704480658206329986017741425592739598784901147490262698283265202147593817926551998457936217729984043905483806898514062338649654338829045552688587285851621946053376392312680578795692682905599590422046720587710762927130740460442438533124053848898103790124491L\nsb."

    def setUp(self):
        global RSA
        global Random
        global bytes_to_long
        from Crypto.PublicKey import RSA
        from Crypto import Random
        from Crypto.Util.number import bytes_to_long, inverse
        self.n = bytes_to_long(a2b_hex(self.modulus))
        self.p = bytes_to_long(a2b_hex(self.prime_factor))
        self.q = divmod(self.n, self.p)[0]
        self.d = inverse(self.e, (self.p - 1) * (self.q - 1))
        self.u = inverse(self.p, self.q)
        self.rsa = RSA

    def test_generate_1arg(self):
        """RSA (default implementation) generated key (1 argument)"""
        rsaObj = self.rsa.generate(1024)
        self._check_private_key(rsaObj)
        self._exercise_primitive(rsaObj)
        pub = rsaObj.publickey()
        self._check_public_key(pub)
        self._exercise_public_primitive(rsaObj)

    def test_generate_2arg(self):
        """RSA (default implementation) generated key (2 arguments)"""
        rsaObj = self.rsa.generate(1024, Random.new().read)
        self._check_private_key(rsaObj)
        self._exercise_primitive(rsaObj)
        pub = rsaObj.publickey()
        self._check_public_key(pub)
        self._exercise_public_primitive(rsaObj)

    def test_generate_3args(self):
        rsaObj = self.rsa.generate(1024, Random.new().read, e=65537)
        self._check_private_key(rsaObj)
        self._exercise_primitive(rsaObj)
        pub = rsaObj.publickey()
        self._check_public_key(pub)
        self._exercise_public_primitive(rsaObj)
        self.assertEqual(65537, rsaObj.e)

    def test_construct_2tuple(self):
        """RSA (default implementation) constructed key (2-tuple)"""
        pub = self.rsa.construct((self.n, self.e))
        self._check_public_key(pub)
        self._check_encryption(pub)
        self._check_verification(pub)

    def test_construct_3tuple(self):
        """RSA (default implementation) constructed key (3-tuple)"""
        rsaObj = self.rsa.construct((self.n, self.e, self.d))
        self._check_encryption(rsaObj)
        self._check_decryption(rsaObj)
        self._check_signing(rsaObj)
        self._check_verification(rsaObj)

    def test_construct_4tuple(self):
        """RSA (default implementation) constructed key (4-tuple)"""
        rsaObj = self.rsa.construct((self.n, self.e, self.d, self.p))
        self._check_encryption(rsaObj)
        self._check_decryption(rsaObj)
        self._check_signing(rsaObj)
        self._check_verification(rsaObj)

    def test_construct_5tuple(self):
        """RSA (default implementation) constructed key (5-tuple)"""
        rsaObj = self.rsa.construct((self.n, self.e, self.d, self.p, self.q))
        self._check_private_key(rsaObj)
        self._check_encryption(rsaObj)
        self._check_decryption(rsaObj)
        self._check_signing(rsaObj)
        self._check_verification(rsaObj)

    def test_construct_6tuple(self):
        """RSA (default implementation) constructed key (6-tuple)"""
        rsaObj = self.rsa.construct((self.n, self.e, self.d, self.p, self.q, self.u))
        self._check_private_key(rsaObj)
        self._check_encryption(rsaObj)
        self._check_decryption(rsaObj)
        self._check_signing(rsaObj)
        self._check_verification(rsaObj)

    def test_factoring(self):
        rsaObj = self.rsa.construct([self.n, self.e, self.d])
        self.failUnless(rsaObj.p == self.p or rsaObj.p == self.q)
        self.failUnless(rsaObj.q == self.p or rsaObj.q == self.q)
        self.failUnless(rsaObj.q * rsaObj.p == self.n)
        self.assertRaises(ValueError, self.rsa.construct, [self.n, self.e, self.n - 1])

    def test_serialization(self):
        """RSA (default implementation) serialize/unserialize key"""
        rsaObj_orig = self.rsa.generate(1024)
        rsaObj = pickle.loads(pickle.dumps(rsaObj_orig))
        self._check_private_key(rsaObj)
        self._exercise_primitive(rsaObj)
        pub = rsaObj.publickey()
        self._check_public_key(pub)
        self._exercise_public_primitive(rsaObj)
        plaintext = a2b_hex(self.plaintext)
        ciphertext1 = rsaObj_orig.encrypt(plaintext, b(''))
        ciphertext2 = rsaObj.encrypt(plaintext, b(''))
        self.assertEqual(ciphertext1, ciphertext2)

    if not (3, 0) <= sys.version_info < (3, 1, 2, 'final', 0):

        def test_serialization_compat(self):
            """RSA (default implementation) backward compatibility serialization"""
            rsaObj = pickle.loads(b(self.pickled_key_2_3))
            plaintext = a2b_hex(self.plaintext)
            ciphertext = a2b_hex(self.ciphertext)
            ciphertext_result = rsaObj.encrypt(plaintext, b(''))[0]
            self.assertEqual(ciphertext_result, ciphertext)

    def _check_private_key(self, rsaObj):
        self.assertEqual(1, rsaObj.has_private())
        self.assertEqual(1, rsaObj.can_sign())
        self.assertEqual(1, rsaObj.can_encrypt())
        self.assertEqual(1, rsaObj.can_blind())
        self.assertEqual(rsaObj.n, rsaObj.key.n)
        self.assertEqual(rsaObj.e, rsaObj.key.e)
        self.assertEqual(rsaObj.d, rsaObj.key.d)
        self.assertEqual(rsaObj.p, rsaObj.key.p)
        self.assertEqual(rsaObj.q, rsaObj.key.q)
        self.assertEqual(rsaObj.u, rsaObj.key.u)
        self.assertEqual(rsaObj.n, rsaObj.p * rsaObj.q)
        self.assertEqual(1, rsaObj.d * rsaObj.e % ((rsaObj.p - 1) * (rsaObj.q - 1)))
        self.assertEqual(1, rsaObj.p * rsaObj.u % rsaObj.q)
        self.assertEqual(1, rsaObj.p > 1)
        self.assertEqual(1, rsaObj.q > 1)
        self.assertEqual(1, rsaObj.e > 1)
        self.assertEqual(1, rsaObj.d > 1)

    def _check_public_key(self, rsaObj):
        ciphertext = a2b_hex(self.ciphertext)
        self.assertEqual(0, rsaObj.has_private())
        self.assertEqual(1, rsaObj.can_sign())
        self.assertEqual(1, rsaObj.can_encrypt())
        self.assertEqual(1, rsaObj.can_blind())
        self.assertEqual(rsaObj.n, rsaObj.key.n)
        self.assertEqual(rsaObj.e, rsaObj.key.e)
        self.assertEqual(0, hasattr(rsaObj, 'd'))
        self.assertEqual(0, hasattr(rsaObj, 'p'))
        self.assertEqual(0, hasattr(rsaObj, 'q'))
        self.assertEqual(0, hasattr(rsaObj, 'u'))
        self.assertEqual(0, hasattr(rsaObj.key, 'd'))
        self.assertEqual(0, hasattr(rsaObj.key, 'p'))
        self.assertEqual(0, hasattr(rsaObj.key, 'q'))
        self.assertEqual(0, hasattr(rsaObj.key, 'u'))
        self.assertEqual(1, rsaObj.e > 1)
        self.assertRaises(TypeError, rsaObj.sign, ciphertext, b(''))
        self.assertRaises(TypeError, rsaObj.decrypt, ciphertext)
        self.assertEqual(rsaObj.publickey() == rsaObj.publickey(), True)
        self.assertEqual(rsaObj.publickey() != rsaObj.publickey(), False)

    def _exercise_primitive(self, rsaObj):
        ciphertext = a2b_hex(self.ciphertext)
        plaintext = rsaObj.decrypt((ciphertext,))
        new_ciphertext2, = rsaObj.encrypt(plaintext, b(''))
        self.assertEqual(b2a_hex(ciphertext), b2a_hex(new_ciphertext2))
        blinding_factor = Random.new().read(len(ciphertext) - 1)
        blinded_ctext = rsaObj.blind(ciphertext, blinding_factor)
        blinded_ptext = rsaObj.decrypt((blinded_ctext,))
        unblinded_plaintext = rsaObj.unblind(blinded_ptext, blinding_factor)
        self.assertEqual(b2a_hex(plaintext), b2a_hex(unblinded_plaintext))
        signature2 = rsaObj.sign(ciphertext, b(''))
        self.assertEqual((bytes_to_long(plaintext),), signature2)
        self.assertEqual(1, rsaObj.verify(ciphertext, (bytes_to_long(plaintext),)))

    def _exercise_public_primitive(self, rsaObj):
        plaintext = a2b_hex(self.plaintext)
        new_ciphertext2, = rsaObj.encrypt(plaintext, b(''))
        rsaObj.verify(new_ciphertext2, (bytes_to_long(plaintext),))

    def _check_encryption(self, rsaObj):
        plaintext = a2b_hex(self.plaintext)
        ciphertext = a2b_hex(self.ciphertext)
        new_ciphertext2, = rsaObj.encrypt(plaintext, b(''))
        self.assertEqual(b2a_hex(ciphertext), b2a_hex(new_ciphertext2))

    def _check_decryption(self, rsaObj):
        plaintext = a2b_hex(self.plaintext)
        ciphertext = a2b_hex(self.ciphertext)
        new_plaintext = rsaObj.decrypt((ciphertext,))
        self.assertEqual(b2a_hex(plaintext), b2a_hex(new_plaintext))
        blinding_factor = Random.new().read(len(ciphertext) - 1)
        blinded_ctext = rsaObj.blind(ciphertext, blinding_factor)
        blinded_ptext = rsaObj.decrypt((blinded_ctext,))
        unblinded_plaintext = rsaObj.unblind(blinded_ptext, blinding_factor)
        self.assertEqual(b2a_hex(plaintext), b2a_hex(unblinded_plaintext))

    def _check_verification(self, rsaObj):
        signature = bytes_to_long(a2b_hex(self.plaintext))
        message = a2b_hex(self.ciphertext)
        t = (
         signature,)
        self.assertEqual(1, rsaObj.verify(message, t))
        t2 = (
         signature, '')
        self.assertEqual(1, rsaObj.verify(message, t2))

    def _check_signing(self, rsaObj):
        signature = bytes_to_long(a2b_hex(self.plaintext))
        message = a2b_hex(self.ciphertext)
        self.assertEqual((signature,), rsaObj.sign(message, b('')))


class RSAFastMathTest(RSATest):

    def setUp(self):
        RSATest.setUp(self)
        self.rsa = RSA.RSAImplementation(use_fast_math=True)

    def test_generate_1arg(self):
        """RSA (_fastmath implementation) generated key (1 argument)"""
        RSATest.test_generate_1arg(self)

    def test_generate_2arg(self):
        """RSA (_fastmath implementation) generated key (2 arguments)"""
        RSATest.test_generate_2arg(self)

    def test_construct_2tuple(self):
        """RSA (_fastmath implementation) constructed key (2-tuple)"""
        RSATest.test_construct_2tuple(self)

    def test_construct_3tuple(self):
        """RSA (_fastmath implementation) constructed key (3-tuple)"""
        RSATest.test_construct_3tuple(self)

    def test_construct_4tuple(self):
        """RSA (_fastmath implementation) constructed key (4-tuple)"""
        RSATest.test_construct_4tuple(self)

    def test_construct_5tuple(self):
        """RSA (_fastmath implementation) constructed key (5-tuple)"""
        RSATest.test_construct_5tuple(self)

    def test_construct_6tuple(self):
        """RSA (_fastmath implementation) constructed key (6-tuple)"""
        RSATest.test_construct_6tuple(self)

    def test_factoring(self):
        RSATest.test_factoring(self)

    def test_serialization(self):
        """RSA (_fastmath implementation) serialize/unserialize key
        """
        RSATest.test_serialization(self)

    if not (3, 0) <= sys.version_info < (3, 1, 2, 'final', 0):

        def test_serialization_compat(self):
            """RSA (_fastmath implementation) backward compatibility serialization
            """
            RSATest.test_serialization_compat(self)


class RSASlowMathTest(RSATest):

    def setUp(self):
        RSATest.setUp(self)
        self.rsa = RSA.RSAImplementation(use_fast_math=False)

    def test_generate_1arg(self):
        """RSA (_slowmath implementation) generated key (1 argument)"""
        RSATest.test_generate_1arg(self)

    def test_generate_2arg(self):
        """RSA (_slowmath implementation) generated key (2 arguments)"""
        RSATest.test_generate_2arg(self)

    def test_construct_2tuple(self):
        """RSA (_slowmath implementation) constructed key (2-tuple)"""
        RSATest.test_construct_2tuple(self)

    def test_construct_3tuple(self):
        """RSA (_slowmath implementation) constructed key (3-tuple)"""
        RSATest.test_construct_3tuple(self)

    def test_construct_4tuple(self):
        """RSA (_slowmath implementation) constructed key (4-tuple)"""
        RSATest.test_construct_4tuple(self)

    def test_construct_5tuple(self):
        """RSA (_slowmath implementation) constructed key (5-tuple)"""
        RSATest.test_construct_5tuple(self)

    def test_construct_6tuple(self):
        """RSA (_slowmath implementation) constructed key (6-tuple)"""
        RSATest.test_construct_6tuple(self)

    def test_factoring(self):
        RSATest.test_factoring(self)

    def test_serialization(self):
        """RSA (_slowmath implementation) serialize/unserialize key"""
        RSATest.test_serialization(self)

    if not (3, 0) <= sys.version_info < (3, 1, 2, 'final', 0):

        def test_serialization_compat(self):
            """RSA (_slowmath implementation) backward compatibility serialization
            """
            RSATest.test_serialization_compat(self)


def get_tests(config={}):
    tests = []
    tests += list_test_cases(RSATest)
    try:
        from Crypto.PublicKey import _fastmath
        tests += list_test_cases(RSAFastMathTest)
    except ImportError:
        from distutils.sysconfig import get_config_var
        import inspect
        _fm_path = os.path.normpath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../../PublicKey/_fastmath' + get_config_var('SO'))
        if os.path.exists(_fm_path):
            raise ImportError('While the _fastmath module exists, importing ' + 'it failed. This may point to the gmp or mpir shared library ' + 'not being in the path. _fastmath was found at ' + _fm_path)

    if config.get('slow_tests', 1):
        tests += list_test_cases(RSASlowMathTest)
    return tests


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')