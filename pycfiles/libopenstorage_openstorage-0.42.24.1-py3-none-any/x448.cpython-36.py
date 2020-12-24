# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/asymmetric/x448.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 2249 bytes
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons

@six.add_metaclass(abc.ABCMeta)
class X448PublicKey(object):

    @classmethod
    def from_public_bytes(cls, data):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x448_supported():
            raise UnsupportedAlgorithm('X448 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x448_load_public_bytes(data)

    @abc.abstractmethod
    def public_bytes(self, encoding, format):
        """
        The serialized bytes of the public key.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class X448PrivateKey(object):

    @classmethod
    def generate(cls):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x448_supported():
            raise UnsupportedAlgorithm('X448 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x448_generate_key()

    @classmethod
    def from_private_bytes(cls, data):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x448_supported():
            raise UnsupportedAlgorithm('X448 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x448_load_private_bytes(data)

    @abc.abstractmethod
    def public_key(self):
        """
        The serialized bytes of the public key.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        The serialized bytes of the private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key):
        """
        Performs a key exchange operation using the provided peer's public key.
        """
        pass