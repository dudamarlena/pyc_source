# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\eth_addr.py
# Compiled at: 2020-04-16 10:27:36
# Size of source mod 2**32: 2661 bytes
import sha3
from .key_helper import KeyHelper

class EthAddrConst:
    __doc__ = ' Class container for Ethereum address constants. '
    PREFIX = '0x'
    START_BYTE = 24


class EthAddrUtils:
    __doc__ = ' Class container for Ethereum address utility functions. '

    def ChecksumEncode(addr):
        """ Checksum encode the specified address.

        Args:
            addr (str): Address string

        Returns:
            str: Checksum encoded address
        """
        addr_digest = sha3.keccak_256(addr.encode()).hexdigest()
        enc_addr = [c.upper() if int(addr_digest[i], 16) >= 8 else c.lower() for i, c in enumerate(addr)]
        return ''.join(enc_addr)


class EthAddr:
    __doc__ = ' Ethereum address class. It allows the Ethereum address generation. '

    @staticmethod
    def ToAddress(pub_key_bytes):
        """ Get address in Ethereum format.

        Args:
            pub_key_bytes (bytes): Public key bytes

        Returns:
            str: Address string

        Raised:
            ValueError: If the key is not a public uncompressed key
        """
        if not KeyHelper.IsPublicUncompressed(pub_key_bytes):
            raise ValueError('Public uncompressed key is required for Ethereum address')
        addr = sha3.keccak_256(pub_key_bytes).hexdigest()[EthAddrConst.START_BYTE:]
        return EthAddrConst.PREFIX + EthAddrUtils.ChecksumEncode(addr)