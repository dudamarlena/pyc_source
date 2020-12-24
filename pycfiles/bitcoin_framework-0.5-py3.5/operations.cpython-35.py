# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/crypto/hash/operations.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 3320 bytes
"""
Defines commonly used hash operations around Bitcoin

All the methods here are supposed to receive and return bytes objects
"""
import hashlib
RIPEMD160 = 'ripemd160'
CHECKSUM_SIZE = 4
CHECKSUM_FIRST = True

def ripemd160(value):
    """
    Given a value in bytes, calculates its ripemd(value) and
    returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    ripemd = hashlib.new(RIPEMD160)
    ripemd.update(value)
    return ripemd.digest()


def sha256(value):
    """
    Given a value in bytes, calculates its ripemd(value) and
    returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    return hashlib.sha256(value).digest()


def ripemd160_sha256(value):
    """
    Given a value in bytes, calculates its ripemd(sha256(value)) and
    returns it

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: 20-byte hash result
    """
    return ripemd160(sha256(value))


def double_sha256(value):
    """
    Given a value in bytes, calculates its checksum and returns it

    Result is therefore:
        sha256(sha256(value))

    Args:
        value (bytes): bytes to calculate the checksum against

    Returns:
        bytes: double sha256 checksum
    """
    return sha256(sha256(value))


CHECKSUM_FUNC = double_sha256

def checksum(value, func=double_sha256, size=CHECKSUM_SIZE, first=CHECKSUM_FIRST):
    """
    Given a value calculates its checksum. It allows to specify the checksum
    function, if the first or latest bytes must be taken and how many checksum
    bytes have to be taken. Defaults will be used if no value is specified

    Args:
        value (bytes): value to calculate checksum on
        func (function): function to use to generate the checksum hash
        size (int): size in bytes of the checksum
        first (bool): true to take n first bytes, false to take last
    """
    if first:
        return func(value)[:size]
    return func(value)[-size:]


def checksum_validate(value, given_checksum, *args, **kwargs):
    """
    Checks if the given value in bytes has the checksum passed, or raises an
    exception if not. The checksum calculation parameters can be passed too

    Args:
        value (bytes): bytes to calculate the checksum against
        given_checksum (bytes): supposed checksum
        *args, **kwargs: extra arguments for checksum calculation

    Raises:
        ValueError: if checksum doesn't match calculated checksum
    """
    valid_checksum = checksum(value, *args, **kwargs)
    if valid_checksum != given_checksum:
        raise ValueError('Invalid checksum.\n            Calculated checksum is %s, given is %s' % (
         valid_checksum.hex(), given_checksum.hex()))