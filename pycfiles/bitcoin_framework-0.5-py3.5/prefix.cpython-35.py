# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/address/prefix.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 5540 bytes
"""
Defines the prefixes available for addresses in the Bitcoin cryptocurrency
according if they belong to the testnet or to the mainnet

Prefixes extracted from:
    https://en.bitcoin.it/wiki/List_of_address_prefixes
"""
from ..nets import Network
from .types import Types

class Prefixes(object):
    __doc__ = '\n    Defines what prefixes every network must define to use for their addresses\n\n    All prefixes must be bytes objects\n\n    Attributes:\n        p2pkh (bytes): prefix for pubkey hash addresses\n        p2sh (bytes): prefix for pay-to-script hash addresses\n        wif (bytes): prefix for WIF private key / pubkey\n        bip32_pubkey (bytes): prefix for BIP32 public keys\n        bip32_pkey (bytes): prefix for BIP32 private keys\n    '
    __slots__ = ['_p2pkh', '_p2sh', '_wif', '_bip32_pubkey',
     '_bip32_pkey']

    def __init__(self):
        """
        Initializes all prefixes with empty lists
        """
        self._p2pkh = None
        self._p2sh = None
        self._wif = None
        self._bip32_pubkey = None
        self._bip32_pkey = None

    @classmethod
    def _check_type(cls, address, prefix):
        """
        Given an address and a list of prefixes, check if the address starts
        with the prefix and returns true if it's the case or false
        if not

        Args:
            address (bytes): address as a bytes object
            prefix (byte): prefix to check

        Returns:
            bool: True if the address belongs to one of the prefixes
        """
        return prefix is not None and address.startswith(prefix)

    def get_type(self, address):
        """
        Given an address, looks in all prefixes and returns the type of address

        Args:
            address (bytes): address as a bytes object

        Returns:
            Types.
        """
        if self._check_type(address, self._p2pkh):
            return Types.p2pkh
        else:
            if self._check_type(address, self._p2sh):
                return Types.p2sh
            if self._check_type(address, self._wif):
                return Types.wif
            if self._check_type(address, self._bip32_pubkey):
                return Types.bip32_pubkey
            if self._check_type(address, self._bip32_pkey):
                return Types.bip32_pkey
            return Types.unknown

    @property
    def p2pkh(self):
        """ Returns the p2pkh attribute """
        return self._p2pkh

    @property
    def p2sh(self):
        """ Returns the p2sh attribute """
        return self._p2sh

    @property
    def wif(self):
        """ Returns the wif attribute """
        return self._wif

    @property
    def bip32_pubkey(self):
        """ Returns the bip32_pubkey attribute """
        return self._bip32_pubkey

    @property
    def bip32_pkey(self):
        """ Returns the bip32_pkey attribute """
        return self._bip32_pkey

    @property
    def all_prefixes(self):
        """ Returns a list with all prefixes """
        return self._p2pkh + self._p2sh + self._wif + self._bip32_pubkey + self._bip32_pkey


class MainNetPrefixes(Prefixes):
    __doc__ = '\n    Defines the mainNet prefixes for Bitcoin addresses\n    '

    def __init__(self):
        """
        Initializes the class with the values of the mainNet prefixes
        """
        super().__init__()
        self._p2pkh = b'\x00'
        self._p2sh = b'\x05'
        self._wif = b'\x80'
        self._bip32_pubkey = b'\x04\x88\xb2\x1e'
        self._bip32_pkey = b'\x04\x88\xad\xe4'


class TestNetPrefixes(Prefixes):
    __doc__ = '\n    Defines the testNet prefixes for Bitcoin addresses\n    '

    def __init__(self):
        """
        Initializes the class with the values of the testNet prefixes
        """
        super().__init__()
        self._p2pkh = b'o'
        self._p2sh = b'\xc4'
        self._wif = b'\xef'
        self._bip32_pubkey = b'\x045\x87\xcf'
        self._bip32_pkey = b'\x045\x83\x94'


PREFIXES_BY_NETWORK = {Network.mainnet: MainNetPrefixes(), 
 Network.testnet: TestNetPrefixes()}

def get(network, address_type):
    """
    Given the network and the type of address, returns the prefix to use for
    the address

    Args:
        network (Network): network for the address
        address_type (Types): type of the address

    Returns:
        bytes: bytes containing the prefix for the address

    Raises:
        AttributeError: if address type is invalid
    """
    assert PREFIXES_BY_NETWORK.get(network) is not None, 'No addresses\n    available for that network'
    return getattr(PREFIXES_BY_NETWORK[network], address_type)


def guess(address):
    """
    Given an address, tries to guess the network and type of the address and
    returns a tuple containing them, or None if prefix can't be guessed.

    Args:
        address (bytes): address as bytes object to guess its prefix, and
        thefore its type and network

    Returns:
        tuple: containing the network and type or None if prefix couldn't be
        guessed
    """
    address_net = None
    for network, prefixes in PREFIXES_BY_NETWORK.items():
        address_type = prefixes.get_type(address)
        if address_type != Types.unknown:
            address_net = network
            break

    if address_net is None:
        return
    else:
        return (
         address_net, address_type)