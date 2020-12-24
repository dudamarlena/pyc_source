# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/CryptoService.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 12020 bytes
from base64 import b64decode
import bitwarden_simple_cli.enums.EncryptionType as EncryptionType
import bitwarden_simple_cli.models.domain.CipherString as CipherString
import bitwarden_simple_cli.models.domain.DecryptParameters as DecryptParameters
import bitwarden_simple_cli.models.domain.SymmetricCryptoKey as SymmetricCryptoKey
from bitwarden_simple_cli.services.Tools import T
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers.base import Cipher
from hashlib import sha256 as hashlib_sha256
from os import urandom
from sys import version_info
import bitwarden_simple_cli.services.ContainerService as ContainerService
import bitwarden_simple_cli.services.StorageService as StorageService
import hmac
Keys = dict(key='key',
  encOrgKeys='encOrgKeys',
  encPrivateKey='encPrivateKey',
  encKey='encKey',
  keyHash='keyHash')

class CryptoService:
    containerService: ContainerService
    encKey = None
    encKey: SymmetricCryptoKey
    legacyEtmKey: SymmetricCryptoKey
    key = None
    key: SymmetricCryptoKey
    orgKeys = None
    orgKeys: []
    privateKey = None
    privateKey: str
    secureStorageService: object
    storageService: StorageService

    def __init__(self, storage_service: StorageService):
        self.storageService = storage_service
        self.containerService = ContainerService.ContainerService()

    @staticmethod
    def aes_decrypt(data, iv, key):
        cipher = Cipher(AES(key), CBC(iv), default_backend())
        decryptor = cipher.decryptor()
        plain_text = decryptor.update(data) + decryptor.finalize()
        padding = plain_text[(len(plain_text) - 1)]
        return plain_text[:len(plain_text) - padding]

    def aes_decrypt_fast(self, parameters: DecryptParameters):
        return self.aes_decrypt(parameters.data, parameters.iv, parameters.encKey)

    @staticmethod
    def aes_decrypt_fast_parameters(data, iv, mac, key: SymmetricCryptoKey):
        p = DecryptParameters()
        p.encKey = key.encKey
        p.data = b64decode(data)
        p.iv = b64decode(iv)
        p.macData = p.iv + p.data
        if key.macKey:
            p.macKey = key.macKey
        if mac:
            p.mac = b64decode(mac)
        return p

    def aes_decrypt_to_bytes(self, enc_type, data, iv, mac, key):
        key_for_enc = self.get_key_for_encryption(key)
        the_key = self.resolve_legacy_key(enc_type, key_for_enc)
        if the_key.macKey is not None:
            if mac is None:
                return
        else:
            if the_key.encType != enc_type:
                return
            if the_key.macKey:
                if mac:
                    mac_data = iv + data
                    computed_mac = hmac.new(the_key.macKey, mac_data, hashlib_sha256).digest()
                    if computed_mac is None:
                        return
                    if not self.macs_compare(mac, computed_mac):
                        T.error('mac failed')
                        return
        return self.aes_decrypt(data, iv, the_key.encKey)

    def aes_decrypt_to_utf8(self, enc_type, data, iv, mac, key):
        key_for_enc = self.get_key_for_encryption(key)
        the_key = self.resolve_legacy_key(enc_type, key_for_enc)
        if the_key.macKey is not None:
            if mac is None:
                return
        if the_key.encType != enc_type:
            T.error('encType unavailable')
            return
        fast_params = self.aes_decrypt_fast_parameters(data, iv, mac, the_key)
        if fast_params.macKey:
            if fast_params.mac:
                computed_mac = hmac.new(fast_params.macKey, fast_params.macData, hashlib_sha256).digest()
                if not self.macs_compare(computed_mac, fast_params.mac):
                    T.error('mac failed')
                    return
        return self.aes_decrypt_fast(fast_params)

    def decrypt_from_bytes(self, enc_bytes, key):
        enc_type = EncryptionType(enc_bytes[0])
        if enc_type == EncryptionType.AesCbc128_HmacSha256_B64 or enc_type == EncryptionType.AesCbc256_HmacSha256_B64:
            if len(enc_bytes) <= 49:
                return
            iv = enc_bytes[1:17]
            mac = enc_bytes[17:49]
            ct = enc_bytes[49:]
        else:
            if enc_type == EncryptionType.AesCbc256_B64:
                if len(enc_bytes) <= 17:
                    return
                iv = enc_bytes[1:17]
                ct = enc_bytes[17:]
                mac = None
            else:
                return
        return self.aes_decrypt_to_bytes(enc_type, ct, iv, mac, key)

    def decrypt_to_bytes(self, cipher_string: CipherString, key: SymmetricCryptoKey):
        iv = b64decode(cipher_string.iv)
        data = b64decode(cipher_string.data)
        mac = b64decode(cipher_string.mac) if cipher_string.mac else None
        return self.aes_decrypt_to_bytes(cipher_string.encryptionType, data, iv, mac, key)

    def decrypt_to_utf8(self, cipher_string: CipherString, key: SymmetricCryptoKey):
        return self.aes_decrypt_to_utf8(cipher_string.encryptionType, cipher_string.data, cipher_string.iv, cipher_string.mac, key)

    def get_enc_key(self):
        if self.encKey:
            return self.encKey
        else:
            enc_key = self.storageService.get(Keys['encKey'])
            if enc_key is None:
                return
                key = self.get_key()
                if key is None:
                    return
                enc_key_cipher = CipherString(enc_key)
                if enc_key_cipher.encryptionType == EncryptionType.AesCbc256_B64:
                    dec_enc_key = self.decrypt_to_bytes(enc_key_cipher, key)
            elif enc_key_cipher.encryptionType == EncryptionType.AesCbc256_HmacSha256_B64:
                new_key = self.stretch_key(key)
                dec_enc_key = self.decrypt_to_bytes(enc_key_cipher, new_key)
            else:
                raise Exception('Unsupported enc_key type.')
        if dec_enc_key is None:
            return
        self.encKey = SymmetricCryptoKey(dec_enc_key)
        return self.encKey

    def get_key(self):
        if self.key:
            return self.key
        key = self.get_secure_storage_service().get(Keys['key'])
        if key:
            self.key = SymmetricCryptoKey(b64decode(key))
        if key:
            return self.key

    def get_key_for_encryption(self, key):
        if key:
            return key
        enc_key = self.get_enc_key()
        if enc_key:
            return enc_key
        return self.get_key()

    def get_org_key(self, org_id):
        if org_id is None:
            return
        org_keys = self.get_org_keys()
        if org_keys is None or org_id not in org_keys:
            return
        return org_keys.get(org_id)

    def get_org_keys(self):
        if self.orgKeys:
            if len(self.orgKeys) > 0:
                return self.orgKeys
        enc_org_keys = self.storageService.get(Keys['encOrgKeys'])
        if enc_org_keys is None:
            return
        org_keys = {}
        set_key = False
        for orgId in enc_org_keys:
            if orgId not in enc_org_keys:
                continue
            dec_value = self.rsa_decrypt(enc_org_keys[orgId])
            org_keys[orgId] = SymmetricCryptoKey(dec_value)
            set_key = True

        if set_key:
            self.orgKeys = org_keys
        return self.orgKeys

    def get_private_key(self):
        if self.privateKey:
            return self.privateKey
        enc_private_key = self.storageService.get(Keys['encPrivateKey'])
        if enc_private_key is None:
            return
        self.privateKey = self.decrypt_to_bytes(CipherString(enc_private_key), None)
        return self.privateKey

    def get_secure_storage_service(self):
        return self.containerService.get_secure_storage_service()

    def has_key(self):
        return self.get_key() is not None

    @staticmethod
    def hkdf_expand(pseudo_random_key, info=b'', length=32, selected_hash=hashes.SHA256):
        if version_info[0] == 3:
            buffer = lambda x: x
        hash_len = selected_hash().digest_size
        length = int(length)
        if length > 255 * hash_len:
            raise Exception('Cannot expand to more than 255 * %d = %d bytes using the specified hash function' % (
             hash_len, 255 * hash_len))
        blocks_needed = length // hash_len + (0 if length % hash_len == 0 else 1)
        okm = b''
        output_block = b''
        for counter in range(blocks_needed):
            output_block = hmac.new(pseudo_random_key, buffer(output_block + info + bytearray((counter + 1,))), selected_hash.name).digest()
            okm += output_block

        return okm[:length]

    @staticmethod
    def macs_compare(a, b):
        key = urandom(32)
        hmac1 = hmac.new(key, a, hashlib_sha256).digest()
        hmac2 = hmac.new(key, b, hashlib_sha256).digest()
        return hmac.compare_digest(hmac1, hmac2)

    def resolve_legacy_key(self, enc_type: EncryptionType, key: SymmetricCryptoKey) -> SymmetricCryptoKey:
        if enc_type == EncryptionType.AesCbc128_HmacSha256_B64:
            if key.encType == EncryptionType.AesCbc256_B64:
                if self.legacyEtmKey is None:
                    self.legacyEtmKey = SymmetricCryptoKey(key.key, EncryptionType.AesCbc128_HmacSha256_B64)
                return self.legacyEtmKey
        return key

    def rsa_decrypt(self, enc_value):
        header_pieces = enc_value.split('.')
        enc_type = None
        enc_pieces = None
        if len(header_pieces) == 1:
            enc_type = EncryptionType.Rsa2048_OaepSha256_B64
            enc_pieces = [header_pieces[0]]
        else:
            if len(header_pieces) == 2:
                try:
                    enc_type = EncryptionType(int(header_pieces[0]))
                    enc_pieces = header_pieces[1].split('|')
                except Exception as e:
                    try:
                        T.error(e)
                    finally:
                        e = None
                        del e

            elif enc_type != EncryptionType.Rsa2048_OaepSha256_B64:
                if enc_type != EncryptionType.Rsa2048_OaepSha1_B64:
                    if enc_type != EncryptionType.Rsa2048_OaepSha256_HmacSha256_B64 and enc_type != EncryptionType.Rsa2048_OaepSha1_HmacSha256_B64:
                        raise Exception('encType unavailable')
            if enc_pieces is None or len(enc_pieces) <= 0:
                raise Exception('encPieces unavailable')
            data = b64decode(enc_pieces[0])
            private_key = self.get_private_key()
            if private_key is None:
                raise Exception('No private key')
            if enc_type == EncryptionType.Rsa2048_OaepSha256_B64 or enc_type == EncryptionType.Rsa2048_OaepSha256_HmacSha256_B64:
                alg = hashes.SHA256()
            else:
                if enc_type == EncryptionType.Rsa2048_OaepSha1_B64 or enc_type == EncryptionType.Rsa2048_OaepSha1_HmacSha256_B64:
                    alg = hashes.SHA1()
                else:
                    raise Exception('encType unavailable.')
            return serialization.load_der_private_key(private_key, None, default_backend()).decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=alg),
              algorithm=alg,
              label=None))

    def stretch_key(self, key: SymmetricCryptoKey):
        new_key = self.hkdf_expand(key.key, b'enc', 32) + self.hkdf_expand(key.key, b'mac', 32)
        return SymmetricCryptoKey(new_key)