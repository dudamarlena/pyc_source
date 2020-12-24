# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/blocks.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1770 bytes
from eth_utils import is_bytes, is_hex, is_integer, is_string, is_text, remove_0x_prefix

def is_predefined_block_number(value):
    if is_text(value):
        value_text = value
    else:
        if is_bytes(value):
            value_text = value.decode('latin-1')
        else:
            if is_integer(value):
                return False
            raise TypeError('unrecognized block reference: %r' % value)
    return value_text in frozenset({'latest', 'pending', 'earliest'})


def is_hex_encoded_block_hash(value):
    if not is_string(value):
        return False
    else:
        return len(remove_0x_prefix(value)) == 64 and is_hex(value)


def is_hex_encoded_block_number(value):
    if not is_string(value):
        return False
    else:
        if is_hex_encoded_block_hash(value):
            return False
        try:
            value_as_int = int(value, 16)
        except ValueError:
            return False

        return 0 <= value_as_int < 2 ** 256


def select_method_for_block_identifier(value, if_hash, if_number, if_predefined):
    if is_predefined_block_number(value):
        return if_predefined
    else:
        if isinstance(value, bytes):
            return if_hash
        else:
            if is_hex_encoded_block_hash(value):
                return if_hash
            if is_integer(value):
                if 0 <= value < 2 ** 256:
                    return if_number
        if is_hex_encoded_block_number(value):
            return if_number
    raise ValueError('Value did not match any of the recognized block identifiers: {0}'.format(value))