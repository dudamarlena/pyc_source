# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\utils.py
# Compiled at: 2020-04-21 02:36:56
# Size of source mod 2**32: 5549 bytes
import binascii, hashlib, hmac
from bisect import bisect_left

def Sha256(data_bytes):
    """ Compute the SHA256 of the specified bytes.

    Args:
        data_bytes (bytes): Data bytes

    Returns:
        bytes: Computed SHA256
    """
    return hashlib.sha256(data_bytes).digest()


def Sha256DigestSize():
    """ Get the SHA256 digest size in bytes.

    Returns:
        int: SHA256 digest size in bytes
    """
    return hashlib.sha256().digest_size


def HmacSha512(key_bytes, data_bytes):
    """ Compute the HMAC-SHA512 of the specified bytes with the specified key.

    Args:
        key_bytes (bytes) : Key bytes
        data_bytes (bytes): Data bytes

    Returns:
        bytes: Computed HMAC-SHA512
    """
    return hmac.new(key_bytes, data_bytes, hashlib.sha512).digest()


def Pbkdf2HmacSha512(password_bytes, salt_bytes, itr_num):
    """ Compute the PBKDF2 HMAC-SHA512 of the specified password, using the specified keys and iteration number.

    Args:
        password_bytes (bytes): Password bytes
        salt_bytes (bytes)    : Salt bytes
        itr_num (int)         : Iteration number

    Returns:
        bytes: Computed PBKDF2 HMAC-SHA512
    """
    return hashlib.pbkdf2_hmac('sha512', password_bytes, salt_bytes, itr_num)


def Hash160(data_bytes):
    """ Compute the Bitcoin Hash-160 of the specified bytes.

    Args:
        data_bytes (bytes): Data bytes

    Returns:
        bytes: Computed Hash-160
    """
    return hashlib.new('ripemd160', hashlib.sha256(data_bytes).digest()).digest()


def BytesToInteger(data_bytes):
    """ Convert the specified bytes to integer.

    Args:
        data_bytes (bytes): Data bytes

    Returns:
        int: Integer representation
    """
    return int(binascii.hexlify(data_bytes), 16)


def BytesToBinaryStr(data_bytes, zero_pad=0):
    """ Convert the specified bytes to a binary string.

    Args:
        data_bytes (bytes)      : Data bytes
        zero_pad (int, optional): Zero padding, 0 if not specified

    Returns:
        str: Binary string
    """
    return IntToBinaryStr(BytesToInteger(data_bytes), zero_pad)


def IntToBinaryStr(data_int, zero_pad=0):
    """ Convert the specified integer to a binary string.

    Args:
        data_int (int)          : Data integer
        zero_pad (int, optional): Zero padding, 0 if not specified

    Returns:
        str: Binary string
    """
    return bin(data_int)[2:].zfill(zero_pad)


def BytesFromBinaryStr(data_str, zero_pad=0):
    """ Convert the specified binary string to bytes.

    Args:
        data_str (str)          : Data string
        zero_pad (int, optional): Zero padding, 0 if not specified

    Returns:
        bytes: Bytes representation
    """
    return binascii.unhexlify(hex(int(data_str, 2))[2:].zfill(zero_pad))


def ListToBytes(data_list):
    """ Convert the specified list to bytes

    Args:
        data_list (list): Data list

    Returns:
        bytes: Correspondent bytes representation
    """
    return bytes(bytearray(data_list))


def BytesToHexString(data_bytes, encoding='utf-8'):
    """ Convert bytes to hex string.

    Args:
        data_bytes (str): Data bytes
        encoding (str)  : Encoding type

    Returns:
        str: Bytes converted to hex string
    """
    return binascii.hexlify(data_bytes).decode(encoding)


def HexStringToBytes(data_str):
    """ Convert hex string to bytes.

    Args:
        data_str (str): Data bytes

    Returns
        bytes: Hex string converted to bytes
    """
    return binascii.unhexlify(data_str)


def StringEncode(data_str, encoding='utf-8'):
    """ Encode string to bytes.

    Args:
        data_str (str): Data string
        encoding (str): Encoding type

    Returns:
        bytes: String encoded to bytes
    """
    return data_str.encode(encoding)


def BinarySearch(arr, elem):
    """ Binary search algorithm simply implemented by using the bisect library.

    Args:
        arr (list): list of elements
        elem (any): element to be searched

    Returns:
        int: First index of the element, -1 if not found
    """
    i = bisect_left(arr, elem)
    if i != len(arr):
        if arr[i] == elem:
            return i
    return -1