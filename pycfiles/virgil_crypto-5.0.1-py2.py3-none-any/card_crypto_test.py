# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Imelstorm/Documents/git-repo/virgil-crypto-python/virgil_crypto/tests/card_crypto_test.py
# Compiled at: 2018-11-08 11:52:18
import unittest
from base64 import b64decode
from virgil_crypto.keys import PublicKey
from virgil_crypto.card_crypto import CardCrypto

class CardCryptoTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(CardCryptoTest, self).__init__(*args, **kwargs)
        self.card_crypto = CardCrypto()
        self.test_text = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
        self.test_data = bytearray(self.test_text.encode())
        self.key_pair = self.card_crypto.crypto.generate_keys()
        self.public_key = self.key_pair.public_key
        self.private_key = self.key_pair.private_key

    def test_export_public_key(self):
        self.assertIsNotNone(self.card_crypto.export_public_key(self.public_key))

    def test_export_public_key_empty_key(self):
        self.assertRaises(ValueError, self.card_crypto.export_public_key, None)
        return

    def test_export_public_key_wrong_key(self):
        invalid_pub_key = PublicKey(None, None)
        self.assertRaises(ValueError, self.card_crypto.export_public_key, invalid_pub_key)
        return

    def test_generate_sha512(self):
        test_hash = self.card_crypto.generate_sha512(self.test_data)
        self.assertIsNotNone(test_hash)
        self.assertEqual(b64decode('UVRFAY8h/41lGy4Jm82uLcbhseXLS852XZ2rE7kH8wJvSneUkpu04NmFqwhtWuz78P+T63xMhxEW0wXP0B21dA=='), bytearray(test_hash))

    def test_generate_sha512_with_empty_data(self):
        self.assertRaises(ValueError, self.card_crypto.generate_sha512, None)
        return

    def test_generate_signature(self):
        self.assertIsNotNone(self.card_crypto.generate_signature(self.test_data, self.private_key))

    def test_generate_signature_empty_data(self):
        self.assertRaises(ValueError, self.card_crypto.generate_signature, None, self.private_key)
        return

    def test_generate_signature_wrong_key(self):
        self.assertRaises(ValueError, self.card_crypto.generate_signature, self.test_data, None)
        return

    def test_import_public_key(self):
        exported_public_key = self.card_crypto.export_public_key(self.public_key)
        imported_public_key = self.card_crypto.import_public_key(exported_public_key)
        self.assertEqual(self.public_key, imported_public_key)

    def test_import_public_key_with_empty_data(self):
        self.assertRaises(ValueError, self.card_crypto.import_public_key, None)
        return

    def test_import_public_key_with_wrong_data(self):
        self.assertRaises(RuntimeError, self.card_crypto.import_public_key, self.test_data)

    def test_verify_signature(self):
        test_signature = self.card_crypto.generate_signature(self.test_data, self.private_key)
        self.assertTrue(self.card_crypto.verify_signature(test_signature, self.test_data, self.public_key))

    def test_verify_signature_with_empty_signature(self):
        self.assertRaises(ValueError, self.card_crypto.verify_signature, None, self.test_data, self.public_key)
        return

    def test_verify_signature_with_empty_key(self):
        test_signature = self.card_crypto.generate_signature(self.test_data, self.private_key)
        self.assertRaises(ValueError, self.card_crypto.verify_signature, test_signature, self.test_data, None)
        return

    def test_verify_signature_with_invalid_signature(self):
        test_signature = self.card_crypto.generate_signature(self.test_data, self.private_key)
        self.assertRaises(RuntimeError, self.card_crypto.verify_signature, test_signature[:-2], self.test_data, self.public_key)