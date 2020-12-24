# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/utils.py
# Compiled at: 2017-06-24 06:55:32
# Size of source mod 2**32: 7885 bytes
"""
Utility functions
"""
import codecs, re, idna
from typing import Iterable, Tuple, Union

def camelcase_to_underscore(camelcase: str) -> str:
    """
    Convert a name in CamelCase to non_camel_case

    :param camelcase: CamelCased string
    :return: non_camel_cased string
    """
    s0 = camelcase.replace('-', '_')
    s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', s0)
    s2 = re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1)
    s3 = s2.lower()
    return re.sub('_+', '_', s3)


def camelcase_to_dash(camelcase: str) -> str:
    """
    Convert a name in CamelCase to non-camel-case

    :param camelcase: CamelCased string
    :return: non-camel-cased string
    """
    return camelcase_to_underscore(camelcase).replace('_', '-')


def validate_domain_label(label: str):
    """
    Check if a given string is a valid domain label

    :param label: The domain label
    """
    try:
        idna.alabel(label)
    except idna.IDNAError as e:
        if e.args and 'A-label' in e.args[0]:
            raise ValueError('Invalid label') from None
        else:
            raise ValueError(e.args[0]) from None


def parse_domain_bytes(buffer: bytes, offset: int=0,
                       length: int=None, allow_relative: bool=False) -> Tuple[(int, str)]:
    """
    Extract a single domain name.

    :param buffer: The buffer to read data from
    :param offset: The offset in the buffer where to start reading
    :param length: The amount of data we are allowed to read from the buffer
    :param allow_relative: Allow domain names that do not end with a zero-length label
    :return: The number of bytes used from the buffer and the extracted domain name
    """
    my_offset = 0
    max_offset = length or len(buffer) - offset
    current_labels = []
    while max_offset > my_offset:
        label_length = buffer[(offset + my_offset)]
        my_offset += 1
        if label_length == 0:
            domain_name_bytes = (b'.').join(current_labels) + b'.'
            domain_name = idna.decode(domain_name_bytes)
            if len(domain_name) > 254:
                raise ValueError('Domain too long')
            return (my_offset, domain_name)
        if label_length > 63:
            raise ValueError('Label too long')
        if my_offset + label_length > max_offset:
            raise ValueError('Invalid encoded domain name, exceeds available buffer')
        current_label_bytes = buffer[offset + my_offset:offset + my_offset + label_length]
        my_offset += label_length
        current_labels.append(current_label_bytes)

    if allow_relative:
        domain_name_bytes = (b'.').join(current_labels)
        domain_name = idna.decode(domain_name_bytes)
        if len(domain_name) > 253:
            raise ValueError('Domain too long')
        return (my_offset, domain_name)
    raise ValueError('Domain name must end with a 0-length label')


def parse_domain_list_bytes(buffer: bytes, offset: int=0,
                            length: int=None) -> Tuple[(int, list)]:
    """
    Extract a list of domain names.

    :param buffer: The buffer to read data from
    :param offset: The offset in the buffer where to start reading
    :param length: The amount of data we are allowed to read from the buffer
    :return: The number of bytes used from the buffer and the extracted domain names
    """
    my_offset = 0
    max_offset = length or len(buffer) - offset
    domain_names = []
    while max_offset > my_offset:
        domain_name_len, domain_name = parse_domain_bytes(buffer, offset=offset + my_offset, length=max_offset - my_offset)
        domain_names.append(domain_name)
        my_offset += domain_name_len

    return (my_offset, domain_names)


def encode_domain(domain_name: str, allow_relative: bool=False) -> bytearray:
    """
    Encode a single domain name as a sequence of bytes

    :param domain_name: The domain name
    :param allow_relative: Assume that domain names that don't end with a period are relative and encode them as such
    :return: The encoded domain name as bytes
    """
    if not isinstance(domain_name, str):
        raise ValueError('Domain name must be a string')
    buffer = bytearray()
    if domain_name.endswith('.'):
        domain_name = domain_name.rstrip('.') + '.'
    try:
        domain_name = idna.encode(domain_name).decode('ascii')
    except idna.IDNAError as e:
        if e.args and 'A-label' in e.args[0]:
            raise ValueError('Invalid label') from None
        else:
            raise ValueError(e.args[0]) from None

    if allow_relative:
        if domain_name.endswith('.'):
            domain_name = domain_name.rstrip('.')
            end_with_zero = True
        else:
            end_with_zero = False
    else:
        domain_name = domain_name.rstrip('.')
        end_with_zero = True
    domain_name_parts = domain_name.split('.')
    for label in domain_name_parts:
        validate_domain_label(label)
        label_length = len(label)
        buffer.append(label_length)
        buffer.extend(label.encode('ascii'))

    if end_with_zero:
        buffer.append(0)
    return buffer


def encode_domain_list(domain_names: Iterable[str]) -> bytearray:
    """
    Encode a list of domain names to a sequence of bytes

    :param domain_names: The list of domain names
    :return: The encoded domain names as bytes
    """
    buffer = bytearray()
    for domain_name in domain_names:
        buffer.extend(encode_domain(domain_name))

    return buffer


def normalise_hex(hex_data: Union[(str, bytes)], include_colons: bool=False) -> str:
    """
    Normalise a string containing hexadecimal data

    :param hex_data: Hexadecimal data, either with or without colon separators per byte
    :param include_colons: Whether to include colon separators per byte in the output
    :return: Hexadecimal data in lowercase without colon separators
    """
    if isinstance(hex_data, bytes):
        hex_data = codecs.encode(hex_data, 'hex').decode('ascii')
    if hex_data == '':
        return hex_data
    if re.match('^[0-9A-Fa-f]{2}(:?[0-9A-Fa-f]{2})*$', hex_data):
        hex_data = hex_data.replace(':', '').lower()
        if include_colons:
            hex_data = ':'.join(re.findall('..', hex_data))
        return hex_data
    raise ValueError('Input data is not valid hex data')