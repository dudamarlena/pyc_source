# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Imelstorm/Documents/git-repo/virgil-crypto-python/virgil_crypto/tests/cipher_test.py
# Compiled at: 2018-11-08 11:52:18
import unittest
from virgil_crypto.virgil_crypto_python import VirgilCipher
from virgil_crypto.virgil_crypto_python import VirgilKeyPair

class VirgilCipherTest(unittest.TestCase):

    def test_encrypts_and_decrypts_data(self):
        raw_data = bytearray('test', 'utf-8')
        key_pair1 = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        key_pair2 = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        cipher = VirgilCipher()
        cipher.addKeyRecipient(bytearray('1', 'utf-8'), key_pair1.publicKey())
        cipher.addKeyRecipient(bytearray('2', 'utf-8'), key_pair2.publicKey())
        encrypted_data = cipher.encrypt(raw_data)
        cipher = VirgilCipher()
        decrypted_data1 = cipher.decryptWithKey(encrypted_data, bytearray('1', 'utf-8'), key_pair1.privateKey())
        self.assertEqual(raw_data, bytearray(decrypted_data1))
        decrypted_data2 = cipher.decryptWithKey(encrypted_data, bytearray('2', 'utf-8'), key_pair2.privateKey())
        self.assertEqual(raw_data, bytearray(decrypted_data2))