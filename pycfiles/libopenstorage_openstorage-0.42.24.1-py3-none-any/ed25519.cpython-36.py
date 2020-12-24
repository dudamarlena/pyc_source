# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/asymmetric/ed25519.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 2395 bytes
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
_ED25519_KEY_SIZE = 32
_ED25519_SIG_SIZE = 64

@six.add_metaclass(abc.ABCMeta)
class Ed25519PublicKey(object):

    @classmethod
    def from_public_bytes(cls, data):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)
        return backend.ed25519_load_public_bytes(data)

    @abc.abstractmethod
    def public_bytes(self, encoding, format):
        """
        The serialized bytes of the public key.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature, data):
        """
        Verify the signature.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class Ed25519PrivateKey(object):

    @classmethod
    def generate(cls):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)
        return backend.ed25519_generate_key()

    @classmethod
    def from_private_bytes(cls, data):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)
        return backend.ed25519_load_private_bytes(data)

    @abc.abstractmethod
    def public_key(self):
        """
        The Ed25519PublicKey derived from the private key.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        The serialized bytes of the private key.
        """
        pass

    @abc.abstractmethod
    def sign(self, data):
        """
        Signs the data.
        """
        pass