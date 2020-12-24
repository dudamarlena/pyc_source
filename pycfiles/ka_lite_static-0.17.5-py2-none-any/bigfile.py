# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/rsa/rsa/bigfile.py
# Compiled at: 2018-07-11 18:15:32
"""Large file support

.. deprecated:: 3.4

    The VARBLOCK format is NOT recommended for general use, has been deprecated since
    Python-RSA 3.4, and will be removed in a future release. It's vulnerable to a
    number of attacks:

    1. decrypt/encrypt_bigfile() does not implement `Authenticated encryption`_ nor
       uses MACs to verify messages before decrypting public key encrypted messages.

    2. decrypt/encrypt_bigfile() does not use hybrid encryption (it uses plain RSA)
       and has no method for chaining, so block reordering is possible.

    See `issue #19 on Github`_ for more information.

.. _Authenticated encryption: https://en.wikipedia.org/wiki/Authenticated_encryption
.. _issue #19 on Github: https://github.com/sybrenstuvel/python-rsa/issues/13

This module contains functions to:

    - break a file into smaller blocks, and encrypt them, and store the
      encrypted blocks in another file.

    - take such an encrypted files, decrypt its blocks, and reconstruct the
      original file.

The encrypted file format is as follows, where || denotes byte concatenation:

    FILE := VERSION || BLOCK || BLOCK ...

    BLOCK := LENGTH || DATA

    LENGTH := varint-encoded length of the subsequent data. Varint comes from
    Google Protobuf, and encodes an integer into a variable number of bytes.
    Each byte uses the 7 lowest bits to encode the value. The highest bit set
    to 1 indicates the next byte is also part of the varint. The last byte will
    have this bit set to 0.

This file format is called the VARBLOCK format, in line with the varint format
used to denote the block sizes.

"""
import warnings
from rsa import key, common, pkcs1, varblock
from rsa._compat import byte

def encrypt_bigfile(infile, outfile, pub_key):
    """Encrypts a file, writing it to 'outfile' in VARBLOCK format.

    .. deprecated:: 3.4
        This function was deprecated in Python-RSA version 3.4 due to security issues
        in the VARBLOCK format. See the documentation_ for more information.

    .. _documentation: https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files

    :param infile: file-like object to read the cleartext from
    :param outfile: file-like object to write the crypto in VARBLOCK format to
    :param pub_key: :py:class:`rsa.PublicKey` to encrypt with

    """
    warnings.warn("The 'rsa.bigfile.encrypt_bigfile' function was deprecated in Python-RSA version 3.4 due to security issues in the VARBLOCK format. See https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files for more information.", DeprecationWarning, stacklevel=2)
    if not isinstance(pub_key, key.PublicKey):
        raise TypeError('Public key required, but got %r' % pub_key)
    key_bytes = common.bit_size(pub_key.n) // 8
    blocksize = key_bytes - 11
    outfile.write(byte(varblock.VARBLOCK_VERSION))
    for block in varblock.yield_fixedblocks(infile, blocksize):
        crypto = pkcs1.encrypt(block, pub_key)
        varblock.write_varint(outfile, len(crypto))
        outfile.write(crypto)


def decrypt_bigfile(infile, outfile, priv_key):
    """Decrypts an encrypted VARBLOCK file, writing it to 'outfile'

    .. deprecated:: 3.4
        This function was deprecated in Python-RSA version 3.4 due to security issues
        in the VARBLOCK format. See the documentation_ for more information.

    .. _documentation: https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files

    :param infile: file-like object to read the crypto in VARBLOCK format from
    :param outfile: file-like object to write the cleartext to
    :param priv_key: :py:class:`rsa.PrivateKey` to decrypt with

    """
    warnings.warn("The 'rsa.bigfile.decrypt_bigfile' function was deprecated in Python-RSA version 3.4 due to security issues in the VARBLOCK format. See https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files for more information.", DeprecationWarning, stacklevel=2)
    if not isinstance(priv_key, key.PrivateKey):
        raise TypeError('Private key required, but got %r' % priv_key)
    for block in varblock.yield_varblocks(infile):
        cleartext = pkcs1.decrypt(block, priv_key)
        outfile.write(cleartext)


__all__ = [
 'encrypt_bigfile', 'decrypt_bigfile']