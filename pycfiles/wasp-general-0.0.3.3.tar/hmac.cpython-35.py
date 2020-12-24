# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/crypto/hmac.py
# Compiled at: 2017-09-12 09:52:35
# Size of source mod 2**32: 2938 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from Crypto.Hash.HMAC import HMAC
import re
from wasp_general.verify import verify_type, verify_value
from wasp_general.crypto.hash import WHash

class WHMAC:
    __doc__ = ' Class that wraps PyCrypto HMAC implementation\n\n\tsee also https://en.wikipedia.org/wiki/Hash-based_message_authentication_code\n\t'
    __default_generator_name__ = 'SHA512'
    __hmac_name_re__ = re.compile('HMAC[\\-_]([a-zA-Z0-9]+)')

    @verify_type(digest_generator=(str, None))
    def __init__(self, digest_generator_name=None):
        """ Create new "code-authenticator"

                :param digest_generator_name: name of hash function
                """
        if digest_generator_name is None:
            digest_generator_name = WHMAC.__default_generator_name__
        if digest_generator_name not in WHash.available_generators():
            raise ValueError('Unknown hash generator: "%s"' % digest_generator_name)
        self._WHMAC__digest_generator = WHash.generator(digest_generator_name)

    def digest_generator(self):
        """ Return hash-generator

                :return: PyCrypto class
                """
        return self._WHMAC__digest_generator

    @verify_type(key=bytes, message=(bytes, None), digest_generator=(str, None))
    def hash(self, key, message=None):
        """ Return digest of the given message and key

                :param key: secret HMAC key
                :param message: code (message) to authenticate

                :return: bytes
                """
        generator = self.digest_generator()
        return HMAC(key, msg=message, digestmod=generator().pycrypto()).digest()

    @classmethod
    @verify_type(name=str)
    @verify_value(name=lambda x: WHMAC.__hmac_name_re__.match(x) is not None)
    def hmac(cls, name):
        """ Return new WHMAC object by the given algorithm name like 'HMAC-SHA256' or 'HMAC_SHA1'

                :param name: name of HMAC algorithm

                :return: WHMAC
                """
        return WHMAC(cls.__hmac_name_re__.search(name).group(1))