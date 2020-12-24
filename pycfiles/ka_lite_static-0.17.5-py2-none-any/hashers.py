# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/tests/hashers.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from django.conf.global_settings import PASSWORD_HASHERS as default_hashers
from django.contrib.auth.hashers import is_password_usable, check_password, make_password, PBKDF2PasswordHasher, load_hashers, PBKDF2SHA1PasswordHasher, get_hasher, identify_hasher, UNUSABLE_PASSWORD
from django.utils import unittest
from django.utils.unittest import skipUnless
try:
    import crypt
except ImportError:
    crypt = None

try:
    import bcrypt
    if not hasattr(bcrypt, b'_bcrypt'):
        bcrypt = None
except ImportError:
    bcrypt = None

class TestUtilsHashPass(unittest.TestCase):

    def setUp(self):
        load_hashers(password_hashers=default_hashers)

    def test_simple(self):
        encoded = make_password(b'lètmein')
        self.assertTrue(encoded.startswith(b'pbkdf2_sha256$'))
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))

    def test_pkbdf2(self):
        encoded = make_password(b'lètmein', b'seasalt', b'pbkdf2_sha256')
        self.assertEqual(encoded, b'pbkdf2_sha256$10000$seasalt$CWWFdHOWwPnki7HvkcqN9iA2T3KLW1cf2uZ5kvArtVY=')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'pbkdf2_sha256')

    def test_sha1(self):
        encoded = make_password(b'lètmein', b'seasalt', b'sha1')
        self.assertEqual(encoded, b'sha1$seasalt$cff36ea83f5706ce9aa7454e63e431fc726b2dc8')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'sha1')

    def test_md5(self):
        encoded = make_password(b'lètmein', b'seasalt', b'md5')
        self.assertEqual(encoded, b'md5$seasalt$3f86d0d3d465b7b458c231bf3555c0e3')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'md5')

    def test_unsalted_md5(self):
        encoded = make_password(b'lètmein', b'', b'unsalted_md5')
        self.assertEqual(encoded, b'88a434c88cca4e900f7874cd98123f43')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'unsalted_md5')
        alt_encoded = b'md5$$%s' % encoded
        self.assertTrue(is_password_usable(alt_encoded))
        self.assertTrue(check_password(b'lètmein', alt_encoded))
        self.assertFalse(check_password(b'lètmeinz', alt_encoded))

    def test_unsalted_sha1(self):
        encoded = make_password(b'lètmein', b'', b'unsalted_sha1')
        self.assertEqual(encoded, b'sha1$$6d138ca3ae545631b3abd71a4f076ce759c5700b')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'unsalted_sha1')
        alt_encoded = encoded[6:]
        self.assertFalse(check_password(b'lètmein', alt_encoded))

    @skipUnless(crypt, b'no crypt module to generate password.')
    def test_crypt(self):
        encoded = make_password(b'lètmei', b'ab', b'crypt')
        self.assertEqual(encoded, b'crypt$$ab1Hv2Lg7ltQo')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password(b'lètmei', encoded))
        self.assertFalse(check_password(b'lètmeiz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'crypt')

    @skipUnless(bcrypt, b'py-bcrypt not installed')
    def test_bcrypt(self):
        encoded = make_password(b'lètmein', hasher=b'bcrypt')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(encoded.startswith(b'bcrypt$'))
        self.assertTrue(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, b'bcrypt')

    def test_unusable(self):
        encoded = make_password(None)
        self.assertFalse(is_password_usable(encoded))
        self.assertFalse(check_password(None, encoded))
        self.assertFalse(check_password(UNUSABLE_PASSWORD, encoded))
        self.assertFalse(check_password(b'', encoded))
        self.assertFalse(check_password(b'lètmein', encoded))
        self.assertFalse(check_password(b'lètmeinz', encoded))
        self.assertRaises(ValueError, identify_hasher, encoded)
        return

    def test_bad_algorithm(self):

        def doit():
            make_password(b'lètmein', hasher=b'lolcat')

        self.assertRaises(ValueError, doit)
        self.assertRaises(ValueError, identify_hasher, b'lolcat$salt$hash')

    def test_bad_encoded(self):
        self.assertFalse(is_password_usable(b'lètmein_badencoded'))
        self.assertFalse(is_password_usable(b''))

    def test_low_level_pkbdf2(self):
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(b'lètmein', b'seasalt')
        self.assertEqual(encoded, b'pbkdf2_sha256$10000$seasalt$CWWFdHOWwPnki7HvkcqN9iA2T3KLW1cf2uZ5kvArtVY=')
        self.assertTrue(hasher.verify(b'lètmein', encoded))

    def test_low_level_pbkdf2_sha1(self):
        hasher = PBKDF2SHA1PasswordHasher()
        encoded = hasher.encode(b'lètmein', b'seasalt')
        self.assertEqual(encoded, b'pbkdf2_sha1$10000$seasalt$oAfF6vgs95ncksAhGXOWf4Okq7o=')
        self.assertTrue(hasher.verify(b'lètmein', encoded))

    def test_upgrade(self):
        self.assertEqual(b'pbkdf2_sha256', get_hasher(b'default').algorithm)
        for algo in ('sha1', 'md5'):
            encoded = make_password(b'lètmein', hasher=algo)
            state = {b'upgraded': False}

            def setter(password):
                state[b'upgraded'] = True

            self.assertTrue(check_password(b'lètmein', encoded, setter))
            self.assertTrue(state[b'upgraded'])

    def test_no_upgrade(self):
        encoded = make_password(b'lètmein')
        state = {b'upgraded': False}

        def setter():
            state[b'upgraded'] = True

        self.assertFalse(check_password(b'WRONG', encoded, setter))
        self.assertFalse(state[b'upgraded'])

    def test_no_upgrade_on_incorrect_pass(self):
        self.assertEqual(b'pbkdf2_sha256', get_hasher(b'default').algorithm)
        for algo in ('sha1', 'md5'):
            encoded = make_password(b'lètmein', hasher=algo)
            state = {b'upgraded': False}

            def setter():
                state[b'upgraded'] = True

            self.assertFalse(check_password(b'WRONG', encoded, setter))
            self.assertFalse(state[b'upgraded'])