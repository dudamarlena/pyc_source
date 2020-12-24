# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/keyvault/public/libnaclkey.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
import libnacl, libnacl.encode, libnacl.public, libnacl.sign
from ...keyvault.keys import PublicKey

class LibNaCLPK(PublicKey):
    """
    A LibNaCL implementation of a public key.
    """

    def __init__(self, binarykey='', pk=None, hex_vk=None):
        """
        Create a new LibNaCL public key. Optionally load it from a string representation or
        using a public key and verification key.

        :param binarykey: load the pk from this string (see key_to_bin())
        :param pk: the libnacl public key to use in byte format
        :param hex_vk: a verification key in hex format
        """
        if binarykey:
            pk, vk = binarykey[:libnacl.crypto_box_SECRETKEYBYTES], binarykey[libnacl.crypto_box_SECRETKEYBYTES:libnacl.crypto_box_SECRETKEYBYTES + libnacl.crypto_sign_SEEDBYTES]
            hex_vk = libnacl.encode.hex_encode(vk)
        self.key = libnacl.public.PublicKey(pk)
        self.veri = libnacl.sign.Verifier(hex_vk)

    def verify(self, signature, msg):
        """
        Verify whether a given signature is correct for a message.

        :param signature: the given signature
        :param msg: the given message
        """
        return self.veri.verify(signature + msg)

    def key_to_bin(self):
        """
        Get the string representation of this key.
        """
        return 'LibNaCLPK:' + self.key.pk + self.veri.vk

    def get_signature_length(self):
        """
        Returns the length, in bytes, of each signature made using EC.
        """
        return libnacl.crypto_sign_BYTES