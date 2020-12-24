# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstorebase/account.py
# Compiled at: 2019-03-20 14:33:32
# Size of source mod 2**32: 3455 bytes
import hashlib, sys
from binascii import hexlify, unhexlify
from graphenebase.account import Address as GPHAddress
from graphenebase.account import BrainKey as GPHBrainKey
from graphenebase.account import PasswordKey as GPHPasswordKey
from graphenebase.account import PrivateKey as GPHPrivateKey
from graphenebase.account import PublicKey as GPHPublicKey
from graphenebase.account import Prefix
default_prefix = 'DST'

class PasswordKey(GPHPasswordKey):
    __doc__ = ' This class derives a private key given the account name, the\n        role and a password. It leverages the technology of Brainkeys\n        and allows people to have a secure private key by providing a\n        passphrase only.\n    '
    prefix = default_prefix


class BrainKey(GPHBrainKey):
    __doc__ = 'Brainkey implementation similar to the graphene-ui web-wallet.\n\n        :param str brainkey: Brain Key\n        :param int sequence: Sequence number for consecutive keys\n\n        Keys in Graphene are derived from a seed brain key which is a string of\n        16 words out of a predefined dictionary with 49744 words. It is a\n        simple single-chain key derivation scheme that is not compatible with\n        BIP44 but easy to use.\n\n        Given the brain key, a private key is derived as::\n\n            privkey = SHA256(SHA512(brainkey + " " + sequence))\n\n        Incrementing the sequence number yields a new key that can be\n        regenerated given the brain key.\n    '
    prefix = default_prefix


class Address(GPHAddress):
    __doc__ = ' Address class\n\n        This class serves as an address representation for Public Keys.\n\n        :param str address: Base58 encoded address (defaults to ``None``)\n        :param str pubkey: Base58 encoded pubkey (defaults to ``None``)\n        :param str prefix: Network prefix (defaults to ``DST``)\n\n        Example::\n\n           Address("DSTFN9r6VYzBK8EKtMewfNbfiGCr56pHDBFi")\n\n    '
    prefix = default_prefix


class PublicKey(GPHPublicKey):
    __doc__ = ' This class deals with Public Keys and inherits ``Address``.\n\n        :param str pk: Base58 encoded public key\n        :param str prefix: Network prefix (defaults to ``DST``)\n\n        Example:::\n\n           PublicKey("DST6UtYWWs3rkZGV8JA86qrgkG6tyFksgECefKE1MiH4HkLD8PFGL")\n\n        .. note:: By default, graphene-based networks deal with **compressed**\n                  public keys. If an **uncompressed** key is required, the\n                  method ``unCompressed`` can be used::\n\n                      PublicKey("xxxxx").unCompressed()\n\n    '
    prefix = default_prefix


class PrivateKey(GPHPrivateKey):
    __doc__ = ' Derives the compressed and uncompressed public keys and\n        constructs two instances of ``PublicKey``:\n\n        :param str wif: Base58check-encoded wif key\n        :param str prefix: Network prefix (defaults to ``DST``)\n\n        Example:::\n\n            PrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd")\n\n        Compressed vs. Uncompressed:\n\n        * ``PrivateKey("w-i-f").pubkey``:\n            Instance of ``PublicKey`` using compressed key.\n        * ``PrivateKey("w-i-f").pubkey.address``:\n            Instance of ``Address`` using compressed key.\n        * ``PrivateKey("w-i-f").uncompressed``:\n            Instance of ``PublicKey`` using uncompressed key.\n        * ``PrivateKey("w-i-f").uncompressed.address``:\n            Instance of ``Address`` using uncompressed key.\n\n    '
    prefix = default_prefix