# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/shamir_share.py
# Compiled at: 2019-11-20 10:59:30
# Size of source mod 2**32: 3229 bytes
import hashlib, hmac, os, shamir_mnemonic
from shamir_mnemonic import *
from shamir_mnemonic import _encrypt, _decrypt, _int_from_indices, _int_to_indices
old_rngs = []

def set_random_bytes(rng):
    old_rngs.append(shamir_mnemonic.RANDOM_BYTES)
    shamir_mnemonic.RANDOM_BYTES = rng


def restore_random_bytes():
    if length(old_rngs) > 0:
        shamir_mnemonic.RANDOM_BYTES = old_rngs.pop()


def mnemonic_from_bytes(bytes_data):
    """
    Converts a 32-byte array into mnemonics.
    """
    return mnemonic_from_indices(_int_to_indices(int.from_bytes(bytes_data, 'big'), 8 * len(bytes_data) // RADIX_BITS, RADIX_BITS))


def mnemonic_to_bytes(mnemonic):
    """
    Converts a mnemonic into a 32-byte array.
    """
    wordlength = len(mnemonic.split(' '))
    return _int_from_indices(mnemonic_to_indices(mnemonic)).to_bytes(bits_to_bytes(RADIX_BITS * wordlength), 'big')


def encrypt_shard(passphrase, unencrypted_shard):
    identifier, iteration_exponent, group_index, group_threshold, groups, member_index, member_threshold, value = unencrypted_shard
    encrypted_value = value
    if passphrase is not None:
        encrypted_value = _encrypt(value, passphrase, iteration_exponent, identifier)
    return (
     identifier, iteration_exponent, group_index, group_threshold, groups, member_index, member_threshold, encrypted_value)


def decrypt_shard(passphrase, encrypted_shard):
    identifier, iteration_exponent, group_index, group_threshold, groups, member_index, member_threshold, encrypted_value = encrypted_shard
    decrypted_value = encrypted_value
    if passphrase is not None:
        decrypted_value = _decrypt(encrypted_value, passphrase, iteration_exponent, identifier)
    return (
     identifier, iteration_exponent, group_index, group_threshold, groups, member_index, member_threshold, decrypted_value)


def decrypt_mnemonic(mnemonic, passphrase):
    decoded = decode_mnemonic(mnemonic)
    decrypted = decrypt_shard(passphrase, decoded)
    return encode_mnemonic(*decrypted)


def reencrypt_mnemonic(mnemonic, oldpassphrase, newpassphrase):
    decoded = decode_mnemonic(mnemonic)
    decrypted = decrypt_shard(oldpassphrase, decoded)
    encrypted = encrypt_shard(newpassphrase, decrypted)
    return encode_mnemonic(*encrypted)


def encrypt_mnemonic(mnemonic, passphrase):
    decoded = decode_mnemonic(mnemonic)
    encrypted = encrypt_shard(passphrase, decoded)
    return encode_mnemonic(*encrypted)