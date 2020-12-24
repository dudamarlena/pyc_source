# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Imelstorm/Documents/git-repo/virgil-crypto-python/virgil_crypto/tests/access_token_signer_test.py
# Compiled at: 2018-11-08 11:52:18
import unittest
from virgil_crypto.access_token_signer import AccessTokenSigner

class AccessTokenSignerTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AccessTokenSignerTest, self).__init__(*args, **kwargs)
        self.token = bytearray(('test_token').encode())
        self.signer = AccessTokenSigner()
        key_pair = self.signer.crypto.generate_keys()
        self.private_key = key_pair.private_key
        self.public_key = key_pair.public_key

    def test_generate_token_signature(self):
        self.assertIsNotNone(self.signer.generate_token_signature(self.token, self.private_key))

    def test_generate_token_signature_empty_token(self):
        self.assertRaises(ValueError, self.signer.generate_token_signature, None, self.private_key)
        return

    def test_generate_token_signature_empty_key(self):
        self.assertRaises(ValueError, self.signer.generate_token_signature, self.token, None)
        return

    def test_verify_token_signature(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertTrue(self.signer.verify_token_signature(signature, self.token, self.public_key))

    def test_verify_token_signature_wrong_signature(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertRaises(RuntimeError, self.signer.verify_token_signature, signature[:-2], self.token, self.public_key)
        wrong_key_pair = self.signer.crypto.generate_keys()
        self.assertFalse(self.signer.verify_token_signature(signature, self.token, wrong_key_pair.public_key))

    def test_verify_token_signature_empty_token(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertRaises(ValueError, self.signer.verify_token_signature, signature, None, self.public_key)
        return

    def test_verify_token_signature_empty_key(self):
        signature = self.signer.generate_token_signature(self.token, self.private_key)
        self.assertRaises(ValueError, self.signer.verify_token_signature, signature, self.token, None)
        return