# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/address/wif.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 3801 bytes
"""
Models a WIF (Wallet Import Format) address type, that contains a compressed /
uncompressed private ECDSA key

Information extracted from:
https://en.bitcoin.it/wiki/Wallet_import_format

Tests extracted from:
http://gobittest.appspot.com/PrivateKey
"""
from ..nets import DEFAULT_NETWORK
from .model import Address
from .types import Types
from ..crypto.ecdsa import private_to_public, validate_private_key
from ..crypto.hash import checksum
PREFIX_SIZE = 1
CHECKSUM_SIZE = 4
WIF_UNCOMPRESSED_SIZE = 32
WIF_COMPRESSED_SIZE = 33
PRIVATE_COMPRESSED_SIZE = 32

class WIF(Address):
    __doc__ = '\n    WIF address address. Allows to serialize, deserialize, encode\n    and decode WIF addresses to obtain and set ECDSA private keys in a portable\n    format\n\n    Internal _value field contains the private key and checksum\n    '

    def __init__(self, private_key, addr_net=DEFAULT_NETWORK):
        """
        Initializes a WIF address given the address network and the private
        key as a bytes object

        Args:
            addr_net (Network): network the address operates in
            private_key (bytes): private ECDSA key as bytes object
        """
        assert isinstance(private_key, bytes), 'Private key must be a bytes\n        object'
        super().__init__(Types.wif, addr_net)
        validate_private_key(private_key)
        self._value = private_key + checksum(self._prefix + private_key)

    @classmethod
    def deserialize(cls, address):
        """
        Deserializes the given address as an array of bytes, guessing its
        prefix and saving its info, checking that the prefix type is WIF and
        after that, setting the ECDSA private key value

        Args:
            address (bytes): bytes object containing an address to deserialize

        Returns:
            self: the object with the updated values
        """
        addr_obj = Address.deserialize(address)
        assert addr_obj.type == Types.wif, 'The deserialized address is not\n        a WIF address'
        private_key = addr_obj._value[:-CHECKSUM_SIZE]
        validate_private_key(private_key)
        return cls(private_key, addr_net=addr_obj.network)

    @property
    def private_key(self):
        """
        Extracts the private key from the address

        Source:
        https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
        """
        private_key = self._value[:-CHECKSUM_SIZE]
        if self.compressed:
            private_key = private_key[:PRIVATE_COMPRESSED_SIZE]
        return private_key

    @property
    def public_key(self):
        """ Extracts the public key from the private key contents """
        return private_to_public(self.private_key)

    @property
    def compressed(self):
        """ Calculates if the address is compressed or not """
        return len(self._value[:-CHECKSUM_SIZE]) == WIF_COMPRESSED_SIZE

    @property
    def checksum(self):
        """ Returns the address checksum """
        return self.value[-CHECKSUM_SIZE:]