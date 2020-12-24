# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/crypto/kdf.py
# Compiled at: 2017-09-06 11:50:57
# Size of source mod 2**32: 4294 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from Crypto.Protocol.KDF import PBKDF2
from wasp_general.verify import verify_type, verify_value
from wasp_general.crypto.hmac import WHMAC
from wasp_general.crypto.random import random_bytes

class WPBKDF2:
    __doc__ = ' Wrapper for PyCrypto PBKDF2 implementation with NIST recommendation and HMAC is used as pseudorandom\n\tfunction\n\n\tNIST recommendation can be read here:\n\thttp://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf (Recommendation for Password-Based\n\tKey Derivation)\n\t'
    __minimum_key_length__ = 20
    __minimum_salt_length__ = 16
    __default_salt_length__ = 64
    __default_digest_generator_name__ = 'SHA256'
    __minimum_iterations_count__ = 1000
    __default_iterations_count__ = 1000
    __default_derived_key_length__ = 16

    @verify_type(key=(str, bytes), salt=(bytes, None), derived_key_length=(int, None))
    @verify_type(iterations_count=(int, None), hmac=(WHMAC, None))
    @verify_value(key=lambda x: x is None or len(x) >= WPBKDF2.__minimum_key_length__)
    @verify_value(salt=lambda x: x is None or len(x) >= WPBKDF2.__minimum_salt_length__)
    @verify_value(iterations_count=lambda x: x is None or x >= WPBKDF2.__minimum_iterations_count__)
    def __init__(self, key, salt=None, derived_key_length=None, iterations_count=None, hmac=None):
        """ Generate new key (derived key) with PBKDF2 algorithm

                :param key: password
                :param salt: salt to use (if no salt was specified, then it will be generated automatically)
                :param derived_key_length: length of byte-sequence to generate
                :param iterations_count: iteration count
                :param hmac: WHMAC object to use with PBKDF2
                """
        self._WPBKDF2__salt = salt if salt is not None else self.generate_salt()
        if derived_key_length is None:
            derived_key_length = self.__default_derived_key_length__
        if iterations_count is None:
            iterations_count = self.__default_iterations_count__
        if hmac is None:
            hmac = WHMAC(self.__default_digest_generator_name__)
        self._WPBKDF2__derived_key = PBKDF2(key, self._WPBKDF2__salt, dkLen=derived_key_length, count=iterations_count, prf=hmac.hash)

    def salt(self):
        """ Return salt value (that was given in constructor or created automatically)

                :return: bytes
                """
        return self._WPBKDF2__salt

    def derived_key(self):
        """ Return derived key

                :return: bytes
                """
        return self._WPBKDF2__derived_key

    @classmethod
    @verify_type(length=(int, None))
    @verify_value(length=lambda x: x is None or x >= WPBKDF2.__minimum_salt_length__)
    def generate_salt(cls, length=None):
        """ Generate salt that can be used by this object

                :param length: target salt length

                :return: bytes
                """
        if length is None:
            length = cls.__default_salt_length__
        return random_bytes(length)