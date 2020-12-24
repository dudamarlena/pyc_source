# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/crypto/rsa.py
# Compiled at: 2017-09-12 07:32:08
# Size of source mod 2**32: 5257 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as pyRSA
from wasp_general.verify import verify_type, verify_value
from wasp_general.crypto.hash import WHash

class WRSA:
    __doc__ = ' PyCrypto RSA-encryption wrapper\n\t'
    wrapped_class = pyRSA.generate(bits=1024).__class__

    @staticmethod
    @verify_type(key_length=int)
    @verify_value(key_length=lambda x: x % 256 == 0 and x >= 1024)
    def generate_private(key_length=2048):
        """ Generate new private key (corresponding public key is included)

                :param key_length: same as bits argument in Crypto.PublicKey.RSA.generate function (it must be          a multiple of 256, and no smaller than 1024)
                :return: WRSA.wrapped_class
                """
        return pyRSA.generate(key_length)

    @staticmethod
    @verify_type(key=wrapped_class, password=(str, bytes, None))
    def export_key(key, password=None):
        """ Export key in PEM-format

                :param key: key to export
                :param password: If it is not None, then result will be encrypt with given password. Suitable only              for private key. With public keys this argument does nothing
                :return: bytes
                """
        return key.exportKey('PEM', passphrase=password)

    @staticmethod
    @verify_type(pem_text=(str, bytes), password=(str, bytes, None))
    def import_key(pem_text, password=None):
        """ Import key written in PEM-format

                :param pem_text: PEM data
                :param password: Password with witch PEM-data is encrypted
                :return: RSA.wrapped_class
                """
        return pyRSA.importKey(pem_text, passphrase=password)

    @staticmethod
    @verify_type(private_key=wrapped_class)
    def generate_public(private_key):
        """ Get public key from private one

                :param private_key: source private key
                :return: RSA.wrapper_class
                """
        return private_key.publickey()

    @staticmethod
    @verify_type(binary_chain=bytes, key=wrapped_class, sha_digest_size=int)
    @verify_value(sha_digest_size=lambda x: x in WHash.available_digests(family='SHA'))
    def encrypt(binary_chain, key, sha_digest_size=32):
        """ Encrypt data with key and PKCS1 OAEP protocol

                :param binary_chain: data to encrypt
                :param key: must be public key or private key with builtin public
                :param sha_digest_size: SHA digest size
                :return: bytes
                """
        hash_generator = WHash.generator_by_digest('SHA', sha_digest_size).new()
        cipher = PKCS1_OAEP.new(key, hashAlgo=hash_generator)
        return cipher.encrypt(binary_chain)

    @staticmethod
    @verify_type(binary_chain=bytes, key=wrapped_class, sha_digest_size=int)
    @verify_value(sha_digest_size=lambda x: x in WHash.available_digests(family='SHA'))
    def decrypt(binary_chain, private_key, sha_digest_size=32):
        """ Decrypt data with key and PKCS1 OAEP protocol

                :param binary_chain: data to decrypt
                :param private_key: private key
                :param sha_digest_size: SHA digest size
                :return: bytes
                """
        hash_generator = WHash.generator_by_digest('SHA', sha_digest_size).new()
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=hash_generator)
        return cipher.decrypt(binary_chain)

    @staticmethod
    @verify_type(text=str, key=wrapped_class, sha_digest_size=int)
    @verify_value(sha_digest_size=lambda x: x in WHash.available_digests(family='SHA'))
    def string_encrypt(text, key, sha_digest_size=32):
        """ Encrypt text with given public key and PKCS1 OAEP protocol

                :param text: text to encrypt
                :param key: public key or private key with builtin public
                :param sha_digest_size: SHA digest size
                :return: bytes
                """
        return WRSA.encrypt(text.encode(), key, sha_digest_size)

    @staticmethod
    @verify_type(binary_data=bytes, key=wrapped_class, text_encoding=(str, None), sha_digest_size=int)
    @verify_value(sha_digest_size=lambda x: x in WHash.available_digests(family='SHA'))
    def string_decrypt(binary_data, private_key, text_encoding=None, sha_digest_size=32):
        """ Decrypt binary data with given private key and PKCS1 OAEP protocol

                :param binary_data: data to decrypt
                :param private_key: private key
                :param text_encoding: source string encoding
                :param sha_digest_size: SHA digest size
                :return: str
                """
        binary = WRSA.decrypt(binary_data, private_key, sha_digest_size)
        if text_encoding is not None:
            return binary.decode(text_encoding)
        return binary.decode()