# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\formatters\standard.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ... import SEQUENCE_TYPES
from .formatters import format_ad_timestamp, format_binary, format_boolean, format_integer, format_sid, format_time, format_unicode, format_uuid, format_uuid_le, format_time_with_0_year, format_ad_timedelta
from .validators import validate_integer, validate_time, always_valid, validate_generic_single_value, validate_boolean, validate_ad_timestamp, validate_sid, validate_uuid_le, validate_uuid, validate_zero_and_minus_one_and_positive_int, validate_guid, validate_time_with_0_year, validate_ad_timedelta
standard_formatter = {'1.2.840.113556.1.4.903': (
                            format_binary, None), 
   '1.2.840.113556.1.4.904': (
                            format_unicode, None), 
   '1.2.840.113556.1.4.905': (
                            format_unicode, None), 
   '1.2.840.113556.1.4.906': (
                            format_integer, validate_integer), 
   '1.2.840.113556.1.4.907': (
                            format_binary, None), 
   '1.2.840.113556.1.4.1221': (
                             format_binary, None), 
   '1.2.840.113556.1.4.1362': (
                             format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.1': (
                                  format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.2': (
                                  format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.3': (
                                  format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.4': (
                                  format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.5': (
                                  format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.6': (
                                  format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.7': (
                                  format_boolean, validate_boolean), 
   '1.3.6.1.4.1.1466.115.121.1.8': (
                                  format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.9': (
                                  format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.10': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.11': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.12': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.13': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.14': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.15': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.16': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.17': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.18': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.19': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.20': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.21': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.22': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.23': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.24': (
                                   format_time, validate_time), 
   '1.3.6.1.4.1.1466.115.121.1.25': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.26': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.27': (
                                   format_integer, validate_integer), 
   '1.3.6.1.4.1.1466.115.121.1.28': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.29': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.30': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.31': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.32': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.33': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.34': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.35': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.36': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.37': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.38': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.39': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.40': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.41': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.42': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.43': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.44': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.45': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.46': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.47': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.48': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.49': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.50': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.51': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.52': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.53': (
                                   format_time, validate_time), 
   '1.3.6.1.4.1.1466.115.121.1.54': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.55': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.56': (
                                   format_binary, None), 
   '1.3.6.1.4.1.1466.115.121.1.57': (
                                   format_unicode, None), 
   '1.3.6.1.4.1.1466.115.121.1.58': (
                                   format_unicode, None), 
   '1.3.6.1.1.16.1': (
                    format_uuid, validate_uuid), 
   '1.3.6.1.1.16.4': (
                    format_uuid, validate_uuid), 
   '2.16.840.1.113719.1.1.4.1.501': (
                                   format_uuid, validate_guid), 
   '2.16.840.1.113719.1.1.5.1.0': (
                                 format_binary, None), 
   '2.16.840.1.113719.1.1.5.1.6': (
                                 format_unicode, None), 
   '2.16.840.1.113719.1.1.5.1.12': (
                                  format_binary, None), 
   '2.16.840.1.113719.1.1.5.1.13': (
                                  format_binary, None), 
   '2.16.840.1.113719.1.1.5.1.14': (
                                  format_unicode, None), 
   '2.16.840.1.113719.1.1.5.1.15': (
                                  format_unicode, None), 
   '2.16.840.1.113719.1.1.5.1.16': (
                                  format_binary, None), 
   '2.16.840.1.113719.1.1.5.1.17': (
                                  format_unicode, None), 
   '2.16.840.1.113719.1.1.5.1.19': (
                                  format_time, validate_time), 
   '2.16.840.1.113719.1.1.5.1.22': (
                                  format_integer, validate_integer), 
   '2.16.840.1.113719.1.1.5.1.23': (
                                  format_unicode, None), 
   '2.16.840.1.113719.1.1.5.1.25': (
                                  format_unicode, None), 
   'supportedldapversion': (
                          format_integer, None), 
   'octetstring': (
                 format_binary, validate_uuid_le), 
   '1.2.840.113556.1.4.2': (
                          format_uuid_le, validate_uuid_le), 
   '1.2.840.113556.1.4.13': (
                           format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.26': (
                           format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.49': (
                           format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.51': (
                           format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.52': (
                           format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.60': (
                           format_ad_timedelta, validate_ad_timedelta), 
   '1.2.840.113556.1.4.61': (
                           format_ad_timedelta, validate_ad_timedelta), 
   '1.2.840.113556.1.4.74': (
                           format_ad_timedelta, validate_ad_timedelta), 
   '1.2.840.113556.1.4.78': (
                           format_ad_timedelta, validate_ad_timedelta), 
   '1.2.840.113556.1.4.96': (
                           format_ad_timestamp, validate_zero_and_minus_one_and_positive_int), 
   '1.2.840.113556.1.4.146': (
                            format_sid, validate_sid), 
   '1.2.840.113556.1.4.159': (
                            format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.662': (
                            format_ad_timestamp, validate_ad_timestamp), 
   '1.2.840.113556.1.4.1696': (
                             format_ad_timestamp, validate_ad_timestamp), 
   '1.3.6.1.4.1.42.2.27.8.1.17': (
                                format_time_with_0_year, validate_time_with_0_year)}

def find_attribute_helpers(attr_type, name, custom_formatter):
    """
    Tries to format following the OIDs info and format_helper specification.
    Search for attribute oid, then attribute name (can be multiple), then attribute syntax
    Precedence is:
    1. attribute name
    2. attribute oid(from schema)
    3. attribute names (from oid_info)
    4. attribute syntax (from schema)
    Custom formatters can be defined in Server object and have precedence over the standard_formatters
    If no formatter is found the raw_value is returned as bytes.
    Attributes defined as SINGLE_VALUE in schema are returned as a single object, otherwise are returned as a list of object
    Formatter functions can return any kind of object
    return a tuple (formatter, validator)
    """
    formatter = None
    if custom_formatter and isinstance(custom_formatter, dict):
        if name in custom_formatter:
            formatter = custom_formatter[name]
        if not formatter and attr_type and attr_type.oid in custom_formatter:
            formatter = custom_formatter[attr_type.oid]
        if not formatter and attr_type and attr_type.oid_info:
            if isinstance(attr_type.oid_info[2], SEQUENCE_TYPES):
                for attr_name in attr_type.oid_info[2]:
                    if attr_name in custom_formatter:
                        formatter = custom_formatter[attr_name]
                        break

            elif attr_type.oid_info[2] in custom_formatter:
                formatter = custom_formatter[attr_type.oid_info[2]]
        if not formatter and attr_type and attr_type.syntax in custom_formatter:
            formatter = custom_formatter[attr_type.syntax]
    if not formatter and name in standard_formatter:
        formatter = standard_formatter[name]
    if not formatter and attr_type and attr_type.oid in standard_formatter:
        formatter = standard_formatter[attr_type.oid]
    if not formatter and attr_type and attr_type.oid_info:
        if isinstance(attr_type.oid_info[2], SEQUENCE_TYPES):
            for attr_name in attr_type.oid_info[2]:
                if attr_name in standard_formatter:
                    formatter = standard_formatter[attr_name]
                    break

        elif attr_type.oid_info[2] in standard_formatter:
            formatter = standard_formatter[attr_type.oid_info[2]]
    if not formatter and attr_type and attr_type.syntax in standard_formatter:
        formatter = standard_formatter[attr_type.syntax]
    if formatter is None:
        return (None, None)
    else:
        return formatter


def format_attribute_values(schema, name, values, custom_formatter):
    if not values:
        return []
    else:
        if not isinstance(values, SEQUENCE_TYPES):
            values = [
             values]
        if schema:
            if schema.attribute_types and name in schema.attribute_types:
                attr_type = schema.attribute_types[name]
            else:
                attr_type = None
            attribute_helpers = find_attribute_helpers(attr_type, name, custom_formatter)
            formatter = isinstance(attribute_helpers, tuple) or attribute_helpers
        else:
            formatter = format_unicode if not attribute_helpers[0] else attribute_helpers[0]
        formatted_values = [ formatter(raw_value) for raw_value in values ]
        if formatted_values:
            if attr_type and attr_type.single_value:
                return formatted_values[0]
            return formatted_values
        return []
        return


def find_attribute_validator(schema, name, custom_validator):
    if schema:
        if schema.attribute_types and name in schema.attribute_types:
            attr_type = schema.attribute_types[name]
        else:
            attr_type = None
        attribute_helpers = find_attribute_helpers(attr_type, name, custom_validator)
        validator = isinstance(attribute_helpers, tuple) or attribute_helpers
    elif not attribute_helpers[1]:
        if attr_type and attr_type.single_value:
            validator = validate_generic_single_value
        else:
            validator = always_valid
    else:
        validator = attribute_helpers[1]
    return validator