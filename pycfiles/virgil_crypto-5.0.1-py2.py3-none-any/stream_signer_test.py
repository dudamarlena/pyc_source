# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Imelstorm/Documents/git-repo/virgil-crypto-python/virgil_crypto/tests/stream_signer_test.py
# Compiled at: 2018-11-08 11:52:18
import io, unittest
from virgil_crypto.virgil_crypto_python import VirgilKeyPair
from virgil_crypto.virgil_crypto_python import VirgilStreamSigner
from virgil_crypto.streams import VirgilStreamDataSource

class VirgilStreamSignerTest(unittest.TestCase):

    def test_signs_and_verifies_data(self):
        raw_data = bytearray('test', 'utf-8')
        key_pair = VirgilKeyPair.generate(VirgilKeyPair.Type_FAST_EC_ED25519)
        input_stream = io.BytesIO(raw_data)
        source = VirgilStreamDataSource(input_stream)
        signer = VirgilStreamSigner()
        signature = signer.sign(source, key_pair.privateKey())
        input_stream = io.BytesIO(raw_data)
        source = VirgilStreamDataSource(input_stream)
        signer = VirgilStreamSigner()
        is_valid = signer.verify(source, signature, key_pair.publicKey())
        self.assertTrue(is_valid)