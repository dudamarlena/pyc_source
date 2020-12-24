# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\formatters\validators.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from binascii import a2b_hex, hexlify
from datetime import datetime
from calendar import timegm
from uuid import UUID
from struct import pack
from ... import SEQUENCE_TYPES, STRING_TYPES, NUMERIC_TYPES, INTEGER_TYPES
from .formatters import format_time, format_ad_timestamp
from ...utils.conv import to_raw, to_unicode, ldap_escape_to_bytes, escape_bytes

def check_backslash(value):
    if isinstance(value, (bytearray, bytes)):
        if '\\' in value:
            value = value.replace('\\', '\\5C')
    elif isinstance(value, STRING_TYPES):
        if '\\' in value:
            value = value.replace('\\', '\\5C')
    return value


def check_type(input_value, value_type):
    if isinstance(input_value, value_type):
        return True
    if isinstance(input_value, SEQUENCE_TYPES):
        for value in input_value:
            if not isinstance(value, value_type):
                return False

        return True
    return False


def always_valid(input_value):
    return True


def validate_generic_single_value(input_value):
    if not isinstance(input_value, SEQUENCE_TYPES):
        return True
    try:
        if len(input_value) == 1:
            return True
    except Exception:
        pass

    return False


def validate_zero_and_minus_one_and_positive_int(input_value):
    """Accept -1 and 0 only (used by pwdLastSet in AD)
    """
    if not isinstance(input_value, SEQUENCE_TYPES):
        if isinstance(input_value, NUMERIC_TYPES) or isinstance(input_value, STRING_TYPES):
            if int(input_value) >= -1:
                return True
            return False
        return False
    if len(input_value) == 1 and (isinstance(input_value[0], NUMERIC_TYPES) or isinstance(input_value[0], STRING_TYPES)):
        if int(input_value[0]) >= -1:
            return True
        return False
    return False


def validate_integer(input_value):
    if check_type(input_value, (float, bool)):
        return False
    else:
        if check_type(input_value, INTEGER_TYPES):
            return True
            sequence = isinstance(input_value, SEQUENCE_TYPES) or False
            input_value = [input_value]
        else:
            sequence = True
        valid_values = []
        from decimal import Decimal, InvalidOperation
        for element in input_value:
            try:
                value = to_unicode(element) if isinstance(element, bytes) else element
                decimal_value = Decimal(value)
                int_value = int(value)
                if decimal_value == int_value:
                    valid_values.append(int_value)
                else:
                    return False
            except (ValueError, TypeError, InvalidOperation):
                return False

        if sequence:
            return valid_values
        return valid_values[0]


def validate_bytes(input_value):
    return check_type(input_value, bytes)


def validate_boolean(input_value):
    if validate_generic_single_value(input_value):
        if isinstance(input_value, SEQUENCE_TYPES):
            input_value = input_value[0]
        if isinstance(input_value, bool):
            if input_value:
                return 'TRUE'
            else:
                return 'FALSE'
        if str is not bytes and isinstance(input_value, bytes):
            input_value = to_unicode(input_value)
        if isinstance(input_value, STRING_TYPES):
            if input_value.lower() == 'true':
                return 'TRUE'
            if input_value.lower() == 'false':
                return 'FALSE'
    return False


def validate_time_with_0_year(input_value):
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        if str is not bytes:
            if isinstance(element, bytes):
                element = to_unicode(element)
            if isinstance(element, STRING_TYPES) and (element.startswith('0000') or isinstance(format_time(to_raw(element)), datetime)):
                valid_values.append(element)
            else:
                return False
        elif isinstance(element, datetime):
            changed = True
            if element.tzinfo:
                valid_values.append(element.strftime('%Y%m%d%H%M%S%z'))
            else:
                offset = datetime.now() - datetime.utcnow()
                valid_values.append((element - offset).strftime('%Y%m%d%H%M%SZ'))
        else:
            return False

    if changed:
        if sequence:
            return valid_values
        else:
            return valid_values[0]
    else:
        return True


def validate_time(input_value):
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        if str is not bytes and isinstance(element, bytes):
            element = to_unicode(element)
        if isinstance(element, STRING_TYPES):
            if isinstance(format_time(to_raw(element)), datetime):
                valid_values.append(element)
            else:
                return False
        elif isinstance(element, datetime):
            changed = True
            if element.tzinfo:
                valid_values.append(element.strftime('%Y%m%d%H%M%S%z'))
            else:
                offset = datetime.now() - datetime.utcnow()
                valid_values.append((element - offset).strftime('%Y%m%d%H%M%SZ'))
        else:
            return False

    if changed:
        if sequence:
            return valid_values
        else:
            return valid_values[0]
    else:
        return True


def validate_ad_timestamp(input_value):
    """
    Active Directory stores date/time values as the number of 100-nanosecond intervals
    that have elapsed since the 0 hour on January 1, 1601 till the date/time that is being stored.
    The time is always stored in Greenwich Mean Time (GMT) in the Active Directory.
    """
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        if str is not bytes and isinstance(element, bytes):
            element = to_unicode(element)
        if isinstance(element, NUMERIC_TYPES):
            if 0 <= element <= 9223372036854775807:
                valid_values.append(element)
            else:
                return False
        elif isinstance(element, STRING_TYPES):
            if isinstance(format_ad_timestamp(to_raw(element)), datetime):
                valid_values.append(element)
            else:
                return False
        elif isinstance(element, datetime):
            changed = True
            if element.tzinfo:
                valid_values.append(to_raw((timegm(element.utctimetuple()) + 11644473600) * 10000000, encoding='ascii'))
            else:
                offset = datetime.now() - datetime.utcnow()
                valid_values.append(to_raw((timegm((element - offset).timetuple()) + 11644473600) * 10000000, encoding='ascii'))
        else:
            return False

    if changed:
        if sequence:
            return valid_values
        else:
            return valid_values[0]
    else:
        return True


def validate_ad_timedelta(input_value):
    """
    Should be validated like an AD timestamp except that since it is a time
    delta, it is stored as a negative number.
    """
    if not isinstance(input_value, INTEGER_TYPES) or input_value > 0:
        return False
    return validate_ad_timestamp(input_value * -1)


def validate_guid(input_value):
    """
    object guid in uuid format (Novell eDirectory)
    """
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        if isinstance(element, STRING_TYPES):
            try:
                valid_values.append(UUID(element).bytes)
                changed = True
            except ValueError:
                try:
                    valid_values.append(UUID(element.replace('\\', '')).bytes)
                    changed = True
                    continue
                except ValueError:
                    if str is not bytes:
                        pass
                    else:
                        valid_values.append(element)
                        continue

                return False

        elif isinstance(element, (bytes, bytearray)):
            valid_values.append(element)
        else:
            return False

    if changed:
        valid_values = [ check_backslash(value) for value in valid_values ]
        if sequence:
            return valid_values
        return valid_values[0]
    else:
        return True


def validate_uuid(input_value):
    """
    object entryUUID in uuid format
    """
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        if isinstance(element, STRING_TYPES):
            try:
                valid_values.append(str(UUID(element)))
                changed = True
            except ValueError:
                try:
                    valid_values.append(str(UUID(element.replace('\\', ''))))
                    changed = True
                    continue
                except ValueError:
                    if str is not bytes:
                        pass
                    else:
                        valid_values.append(element)
                        continue

                return False

        elif isinstance(element, (bytes, bytearray)):
            valid_values.append(element)
        else:
            return False

    if changed:
        valid_values = [ check_backslash(value) for value in valid_values ]
        if sequence:
            return valid_values
        return valid_values[0]
    else:
        return True


def validate_uuid_le(input_value):
    """
    Active Directory stores objectGUID in uuid_le format, follows RFC4122 and MS-DTYP:
    "{07039e68-4373-264d-a0a7-07039e684373}": string representation big endian, converted to little endian (with or without brace curles)
    "689e030773434d26a7a007039e684373": packet representation, already in little endian
    "\x068\\9e\x03\x07;#\x04d\x16\x077\x070\x07\x03\\9e\x068#;": bytes representation, already in little endian
    byte sequence: already in little endian

    """
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        error = False
        if isinstance(element, STRING_TYPES):
            if element[0] == '{' and element[(-1)] == '}':
                try:
                    valid_values.append(UUID(hex=element).bytes_le)
                    changed = True
                except ValueError:
                    error = True

            elif '-' in element:
                try:
                    valid_values.append(UUID(hex=element).bytes_le)
                    changed = True
                except ValueError:
                    error = True

            elif '\\' in element:
                try:
                    uuid = UUID(bytes_le=ldap_escape_to_bytes(element)).bytes_le
                    uuid = escape_bytes(uuid)
                    valid_values.append(uuid)
                    changed = True
                except ValueError:
                    error = True

            elif '-' not in element:
                try:
                    valid_values.append(UUID(bytes_le=a2b_hex(element)).bytes_le)
                    changed = True
                except ValueError:
                    error = True

            if error and str == bytes:
                valid_values.append(element)
        elif isinstance(element, (bytes, bytearray)):
            valid_values.append(element)
        else:
            return False

    if changed:
        valid_values = [ check_backslash(value) for value in valid_values ]
        if sequence:
            return valid_values
        return valid_values[0]
    else:
        return True


def validate_sid(input_value):
    """
        SID= "S-1-" IdentifierAuthority 1*SubAuthority
               IdentifierAuthority= IdentifierAuthorityDec / IdentifierAuthorityHex
                  ; If the identifier authority is < 2^32, the
                  ; identifier authority is represented as a decimal
                  ; number
                  ; If the identifier authority is >= 2^32,
                  ; the identifier authority is represented in
                  ; hexadecimal
                IdentifierAuthorityDec =  1*10DIGIT
                  ; IdentifierAuthorityDec, top level authority of a
                  ; security identifier is represented as a decimal number
                IdentifierAuthorityHex = "0x" 12HEXDIG
                  ; IdentifierAuthorityHex, the top-level authority of a
                  ; security identifier is represented as a hexadecimal number
                SubAuthority= "-" 1*10DIGIT
                  ; Sub-Authority is always represented as a decimal number
                  ; No leading "0" characters are allowed when IdentifierAuthority
                  ; or SubAuthority is represented as a decimal number
                  ; All hexadecimal digits must be output in string format,
                  ; pre-pended by "0x"

        Revision (1 byte): An 8-bit unsigned integer that specifies the revision level of the SID. This value MUST be set to 0x01.
        SubAuthorityCount (1 byte): An 8-bit unsigned integer that specifies the number of elements in the SubAuthority array. The maximum number of elements allowed is 15.
        IdentifierAuthority (6 bytes): A SID_IDENTIFIER_AUTHORITY structure that indicates the authority under which the SID was created. It describes the entity that created the SID. The Identifier Authority value {0,0,0,0,0,5} denotes SIDs created by the NT SID authority.
        SubAuthority (variable): A variable length array of unsigned 32-bit integers that uniquely identifies a principal relative to the IdentifierAuthority. Its length is determined by SubAuthorityCount.

        If you have a SID like S-a-b-c-d-e-f-g-...

        Then the bytes are
        a       (revision)
        N       (number of dashes minus two)
        bbbbbb  (six bytes of "b" treated as a 48-bit number in big-endian format)
        cccc    (four bytes of "c" treated as a 32-bit number in little-endian format)
        dddd    (four bytes of "d" treated as a 32-bit number in little-endian format)
        eeee    (four bytes of "e" treated as a 32-bit number in little-endian format)
        ffff    (four bytes of "f" treated as a 32-bit number in little-endian format)

    """
    if not isinstance(input_value, SEQUENCE_TYPES):
        sequence = False
        input_value = [input_value]
    else:
        sequence = True
    valid_values = []
    changed = False
    for element in input_value:
        if isinstance(element, STRING_TYPES):
            if element.startswith('S-'):
                parts = element.split('-')
                sid_bytes = pack('<q', int(parts[1]))[0:1]
                sid_bytes += pack('<q', len(parts[3:]))[0:1]
                if len(parts[2]) <= 10:
                    sid_bytes += pack('>q', int(parts[2]))[2:]
                else:
                    sid_bytes += pack('>q', int(parts[2], 16))[2:]
                for sub_auth in parts[3:]:
                    sid_bytes += pack('<q', int(sub_auth))[0:4]

                valid_values.append(sid_bytes)
                changed = True

    if changed:
        valid_values = [ check_backslash(value) for value in valid_values ]
        if sequence:
            return valid_values
        return valid_values[0]
    else:
        return True