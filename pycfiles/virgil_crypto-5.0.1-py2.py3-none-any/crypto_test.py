# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Imelstorm/Documents/git-repo/virgil-crypto-python/virgil_crypto/tests/crypto_test.py
# Compiled at: 2018-11-08 11:52:18
import io, unittest
from virgil_crypto import crypto
from virgil_crypto import VirgilCrypto
from virgil_crypto.hashes import HashAlgorithm

class CryptoTest(unittest.TestCase):

    def _crypto(self):
        return VirgilCrypto()

    def test_strtobytes(self):
        self.assertEqual(self._crypto().strtobytes('test'), (116, 101, 115, 116))

    def test_import_private_key(self):
        key_pair = self._crypto().generate_keys()
        private_key_data = key_pair.private_key.raw_key
        self.assertEqual(self._crypto().import_private_key(private_key_data), key_pair.private_key)

    def test_import_public_key(self):
        key_pair = self._crypto().generate_keys()
        public_key_data = key_pair.public_key.raw_key
        self.assertEqual(self._crypto().import_public_key(public_key_data), key_pair.public_key)

    def test_export_and_import_private_key_with_password(self):
        password = '123456'
        key_pair = self._crypto().generate_keys()
        exported_private_key = self._crypto().export_private_key(key_pair.private_key, password)
        self.assertNotEqual(exported_private_key, key_pair.private_key.raw_key)
        imported_private_key = self._crypto().import_private_key(exported_private_key, password)
        self.assertEqual(imported_private_key, key_pair.private_key)

    def test_export_public_key(self):
        key_pair = self._crypto().generate_keys()
        exported_public_key = self._crypto().export_public_key(key_pair.public_key)
        self.assertEqual(exported_public_key, key_pair.public_key.raw_key)

    def test_extract_public_key(self):
        key_pair = self._crypto().generate_keys()
        extracted_public_key = self._crypto().extract_public_key(key_pair.private_key)
        self.assertEqual(extracted_public_key, key_pair.public_key)

    def test_encrypt_and_decrypt_values(self):
        data = [
         1, 2, 3]
        key_pair = self._crypto().generate_keys()
        encrypt_result = self._crypto().encrypt(data, key_pair.public_key)
        decrypt_result = self._crypto().decrypt(encrypt_result, key_pair.private_key)
        self.assertEqual(data, list(decrypt_result))

    def test_encrypt_and_decrypt_stream(self):
        data = bytearray([1, 2, 3])
        key_pair = self._crypto().generate_keys()
        encrypt_input_stream = io.BytesIO(data)
        encrypt_output_stream = io.BytesIO()
        self._crypto().encrypt_stream(encrypt_input_stream, encrypt_output_stream, key_pair.public_key)
        encrypt_stream_result = encrypt_output_stream.getvalue()
        decrypt_input_stream = io.BytesIO(encrypt_stream_result)
        decrypt_output_stream = io.BytesIO()
        self._crypto().decrypt_stream(decrypt_input_stream, decrypt_output_stream, key_pair.private_key)
        decrypt_stream_result = decrypt_output_stream.getvalue()
        self.assertEqual(data, decrypt_stream_result)

    def test_sign_and_verify_values(self):
        data = [
         1, 2, 3]
        key_pair = self._crypto().generate_keys()
        signature = self._crypto().sign(data, key_pair.private_key)
        verified = self._crypto().verify(data, signature, key_pair.public_key)
        self.assertTrue(verified)

    def test_sign_and_verify_values_sha265(self):
        data = [
         1, 2, 3]
        cr = self._crypto()
        cr.signature_hash_algorithm = HashAlgorithm.SHA256
        key_pair = cr.generate_keys()
        signature = cr.sign(data, key_pair.private_key)
        verified = cr.verify(data, signature, key_pair.public_key)
        self.assertTrue(verified)

    def test_sign_and_verify_stream(self):
        data = bytearray([1, 2, 3])
        key_pair = self._crypto().generate_keys()
        sign_input_stream = io.BytesIO(data)
        signature = self._crypto().sign_stream(sign_input_stream, key_pair.private_key)
        verify_input_stream = io.BytesIO(data)
        verified = self._crypto().verify_stream(verify_input_stream, signature, key_pair.public_key)
        self.assertTrue(verified)

    def test_sign_and_verify_stream_sha256(self):
        data = bytearray([1, 2, 3])
        cr = self._crypto()
        cr.signature_hash_algorithm = HashAlgorithm.SHA256
        key_pair = cr.generate_keys()
        sign_input_stream = io.BytesIO(data)
        signature = cr.sign_stream(sign_input_stream, key_pair.private_key)
        verify_input_stream = io.BytesIO(data)
        verified = cr.verify_stream(verify_input_stream, signature, key_pair.public_key)
        self.assertTrue(verified)

    def test_calculate_fingerprint(self):
        data = bytearray([1, 2, 3])
        fingerprint = self._crypto().calculate_fingerprint(data)
        self.assertTrue(fingerprint.value)
        self.assertIsInstance(fingerprint, crypto.Fingerprint)