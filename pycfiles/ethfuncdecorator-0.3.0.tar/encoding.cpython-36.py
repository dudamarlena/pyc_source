# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/encoding.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 6008 bytes
import re
from eth_utils import add_0x_prefix, big_endian_to_int, decode_hex, encode_hex, int_to_big_endian, is_boolean, is_bytes, is_hex, is_integer, remove_0x_prefix, to_hex
from web3.utils.abi import is_address_type, is_array_type, is_bool_type, is_bytes_type, is_int_type, is_string_type, is_uint_type, size_of_type, sub_type_of_array_type
from web3.utils.toolz import curry
from web3.utils.validation import assert_one_val, validate_abi_type, validate_abi_value

def hex_encode_abi_type(abi_type, value, force_size=None):
    """
    Encodes value into a hex string in format of abi_type
    """
    validate_abi_type(abi_type)
    validate_abi_value(abi_type, value)
    data_size = force_size or size_of_type(abi_type)
    if is_array_type(abi_type):
        sub_type = sub_type_of_array_type(abi_type)
        return ''.join([remove_0x_prefix(hex_encode_abi_type(sub_type, v, 256)) for v in value])
    if is_bool_type(abi_type):
        return to_hex_with_size(value, data_size)
    if is_uint_type(abi_type):
        return to_hex_with_size(value, data_size)
    if is_int_type(abi_type):
        return to_hex_twos_compliment(value, data_size)
    if is_address_type(abi_type):
        return pad_hex(value, data_size)
    if is_bytes_type(abi_type):
        if is_bytes(value):
            return encode_hex(value)
        else:
            return value
    else:
        if is_string_type(abi_type):
            return to_hex(text=value)
        raise ValueError('Unsupported ABI type: {0}'.format(abi_type))


def to_hex_twos_compliment(value, bit_size):
    """
    Converts integer value to twos compliment hex representation with given bit_size
    """
    if value >= 0:
        return to_hex_with_size(value, bit_size)
    else:
        value = (1 << bit_size) + value
        hex_value = hex(value)
        hex_value = hex_value.rstrip('L')
        return hex_value


def to_hex_with_size(value, bit_size):
    """
    Converts a value to hex with given bit_size:
    """
    return pad_hex(to_hex(value), bit_size)


def pad_hex(value, bit_size):
    """
    Pads a hex string up to the given bit_size
    """
    value = remove_0x_prefix(value)
    return add_0x_prefix(value.zfill(int(bit_size / 4)))


def trim_hex(hexstr):
    if hexstr.startswith('0x0'):
        hexstr = re.sub('^0x0+', '0x', hexstr)
        if hexstr == '0x':
            hexstr = '0x0'
    return hexstr


def to_int(value=None, hexstr=None, text=None):
    """
    Converts value to it's integer representation.

    Values are converted this way:

     * value:
       * bytes: big-endian integer
       * bool: True => 1, False => 0
     * hexstr: interpret hex as integer
     * text: interpret as string of digits, like '12' => 12
    """
    assert_one_val(value, hexstr=hexstr, text=text)
    if hexstr is not None:
        return int(hexstr, 16)
    else:
        if text is not None:
            return int(text)
        if isinstance(value, bytes):
            return big_endian_to_int(value)
        if isinstance(value, str):
            raise TypeError('Pass in strings with keyword hexstr or text')
        else:
            return int(value)


@curry
def pad_bytes(fill_with, num_bytes, unpadded):
    return unpadded.rjust(num_bytes, fill_with)


zpad_bytes = pad_bytes(b'\x00')

def to_bytes(primitive=None, hexstr=None, text=None):
    assert_one_val(primitive, hexstr=hexstr, text=text)
    if is_boolean(primitive):
        if primitive:
            return b'\x01'
        else:
            return b'\x00'
    if isinstance(primitive, bytes):
        return primitive
    if is_integer(primitive):
        return to_bytes(hexstr=(to_hex(primitive)))
    if hexstr is not None:
        if len(hexstr) % 2:
            hexstr = '0x0' + remove_0x_prefix(hexstr)
        return decode_hex(hexstr)
    if text is not None:
        return text.encode('utf-8')
    raise TypeError('expected an int in first arg, or keyword of hexstr or text')


def to_text(primitive=None, hexstr=None, text=None):
    assert_one_val(primitive, hexstr=hexstr, text=text)
    if hexstr is not None:
        return to_bytes(hexstr=hexstr).decode('utf-8')
    if text is not None:
        return text
    if isinstance(primitive, str):
        return to_text(hexstr=primitive)
    if isinstance(primitive, bytes):
        return primitive.decode('utf-8')
    if is_integer(primitive):
        byte_encoding = int_to_big_endian(primitive)
        return to_text(byte_encoding)
    raise TypeError('Expected an int, bytes or hexstr.')


@curry
def text_if_str(to_type, text_or_primitive):
    """
    Convert to a type, assuming that strings can be only unicode text (not a hexstr)

    @param to_type is a function that takes the arguments (primitive, hexstr=hexstr, text=text),
        eg~ to_bytes, to_text, to_hex, to_int, etc
    @param hexstr_or_primitive in bytes, str, or int.
    """
    if isinstance(text_or_primitive, str):
        primitive, text = None, text_or_primitive
    else:
        primitive, text = text_or_primitive, None
    return to_type(primitive, text=text)


@curry
def hexstr_if_str(to_type, hexstr_or_primitive):
    """
    Convert to a type, assuming that strings can be only hexstr (not unicode text)

    @param to_type is a function that takes the arguments (primitive, hexstr=hexstr, text=text),
        eg~ to_bytes, to_text, to_hex, to_int, etc
    @param text_or_primitive in bytes, str, or int.
    """
    if isinstance(hexstr_or_primitive, str):
        primitive, hexstr = None, hexstr_or_primitive
        if remove_0x_prefix(hexstr):
            if not is_hex(hexstr):
                raise ValueError('when sending a str, it must be a hex string. Got: {0!r}'.format(hexstr_or_primitive))
    else:
        primitive, hexstr = hexstr_or_primitive, None
    return to_type(primitive, hexstr=hexstr)