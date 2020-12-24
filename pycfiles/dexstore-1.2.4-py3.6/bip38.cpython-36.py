# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstorebase/bip38.py
# Compiled at: 2019-03-19 09:04:59
# Size of source mod 2**32: 913 bytes
from graphenebase.bip38 import decrypt as GPHdecrypt
from graphenebase.bip38 import encrypt as GPHencrypt

def encrypt(privkey, passphrase):
    """ BIP0038 non-ec-multiply encryption. Returns BIP0038 encrypted privkey.

    :param privkey: Private key
    :type privkey: Base58
    :param str passphrase: UTF-8 encoded passphrase for encryption
    :return: BIP0038 non-ec-multiply encrypted wif key
    :rtype: Base58

    """
    return GPHencrypt(privkey, passphrase)


def decrypt(encrypted_privkey, passphrase):
    """BIP0038 non-ec-multiply decryption. Returns WIF privkey.

    :param Base58 encrypted_privkey: Private key
    :param str passphrase: UTF-8 encoded passphrase for decryption
    :return: BIP0038 non-ec-multiply decrypted key
    :rtype: Base58
    :raises SaltException: if checksum verification failed (e.g. wrong password)

    """
    return GPHdecrypt(encrypted_privkey, passphrase)