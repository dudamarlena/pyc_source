# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/field/helper.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 1472 bytes
"""
Helper methods to ease the tasks of dealing with bytes in Python and with
Bitcoin fields as bytes in general
"""
HEX_STR_PRE = '0x'
HEX_STR_LEN_MAX = 200

def bfh(hexa):
    """
    Little helper that converts a string of hex-digits into a bytes object

    Args:
        hexa (str): string of hex digits
    Returns:
        bytes: byte object with the contents of the hex string
    """
    return bytes().fromhex(hexa)


def value_to_hex(value):
    """
    Converts a value into a string, trying to set it as an hex string if found
    a bytes object or a number

    Just converts to hex string bytes and bytearray objects, and positive or
    zero integers. The rest of values will return str(value)

    Args:
        value (mixed): value to convert to hex string
    Returns:
        str: hexa string or str(value) if no conversible value found
    """
    value_as_str = str(value)
    if isinstance(value, bytes) or isinstance(value, bytearray):
        value_as_str = HEX_STR_PRE + value.hex()
    elif isinstance(value, int) and value >= 0:
        value_as_str = (HEX_STR_PRE + '{0:02x}').format(value)
    if value_as_str.startswith(HEX_STR_PRE) and len(value_as_str) > HEX_STR_LEN_MAX:
        value_as_str = value_as_str[:HEX_STR_LEN_MAX] + '...'
    return value_as_str