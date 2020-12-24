# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\convert.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from pyasn1.error import PyAsn1Error
from .. import SEQUENCE_TYPES, STRING_TYPES, get_config_parameter
from ..core.exceptions import LDAPControlError, LDAPAttributeError, LDAPObjectClassError, LDAPInvalidValueError
from ..protocol.rfc4511 import Controls, Control
from ..utils.conv import to_raw, to_unicode, escape_filter_chars, is_filter_escaped
from ..protocol.formatters.standard import find_attribute_validator

def attribute_to_dict(attribute):
    try:
        return {'type': str(attribute['type']), 'values': [ str(val) for val in attribute['vals'] ]}
    except PyAsn1Error:
        return {'type': str(attribute['type']), 'values': [ bytes(val) for val in attribute['vals'] ]}


def attributes_to_dict(attributes):
    attributes_dict = dict()
    for attribute in attributes:
        attribute_dict = attribute_to_dict(attribute)
        attributes_dict[attribute_dict['type']] = attribute_dict['values']

    return attributes_dict


def referrals_to_list(referrals):
    if isinstance(referrals, list):
        if referrals:
            return [ str(referral) for referral in referrals if referral ]
        return
    else:
        if referrals is not None and referrals.hasValue():
            return [ str(referral) for referral in referrals if referral ]
        else:
            return
        return


def search_refs_to_list(search_refs):
    if search_refs:
        return [ str(search_ref) for search_ref in search_refs if search_ref ]
    else:
        return


def search_refs_to_list_fast(search_refs):
    if search_refs:
        return [ to_unicode(search_ref) for search_ref in search_refs if search_ref ]
    else:
        return


def sasl_to_dict(sasl):
    return {'mechanism': str(sasl['mechanism']), 'credentials': bytes(sasl['credentials']) if sasl['credentials'] is not None and sasl['credentials'].hasValue() else None}


def authentication_choice_to_dict(authentication_choice):
    return {'simple': str(authentication_choice['simple']) if authentication_choice.getName() == 'simple' else None, 'sasl': sasl_to_dict(authentication_choice['sasl']) if authentication_choice.getName() == 'sasl' else None}


def partial_attribute_to_dict(modification):
    try:
        return {'type': str(modification['type']), 'value': [ str(value) for value in modification['vals'] ]}
    except PyAsn1Error:
        return {'type': str(modification['type']), 'value': [ bytes(value) for value in modification['vals'] ]}


def change_to_dict(change):
    return {'operation': int(change['operation']), 'attribute': partial_attribute_to_dict(change['modification'])}


def changes_to_list(changes):
    return [ change_to_dict(change) for change in changes ]


def attributes_to_list(attributes):
    return [ str(attribute) for attribute in attributes ]


def ava_to_dict(ava):
    try:
        return {'attribute': str(ava['attributeDesc']), 'value': escape_filter_chars(str(ava['assertionValue']))}
    except Exception:
        try:
            return {'attribute': str(ava['attributeDesc']), 'value': escape_filter_chars(bytes(ava['assertionValue']))}
        except Exception:
            return {'attribute': str(ava['attributeDesc']), 'value': bytes(ava['assertionValue'])}


def substring_to_dict(substring):
    return {'initial': substring['initial'] if substring['initial'] else '', 'any': [ middle for middle in substring['any'] ] if substring['any'] else '', 'final': substring['final'] if substring['final'] else ''}


def prepare_changes_for_request(changes):
    prepared = dict()
    for change in changes:
        attribute_name = change['attribute']['type']
        if attribute_name not in prepared:
            prepared[attribute_name] = []
        prepared[attribute_name].append((change['operation'], change['attribute']['value']))

    return prepared


def build_controls_list(controls):
    """controls is a sequence of Control() or sequences
    each sequence must have 3 elements: the control OID, the criticality, the value
    criticality must be a boolean
    """
    if not controls:
        return
    else:
        if not isinstance(controls, SEQUENCE_TYPES):
            raise LDAPControlError('controls must be a sequence')
        built_controls = Controls()
        for (idx, control) in enumerate(controls):
            if isinstance(control, Control):
                built_controls.setComponentByPosition(idx, control)
            elif len(control) == 3 and isinstance(control[1], bool):
                built_control = Control()
                built_control['controlType'] = control[0]
                built_control['criticality'] = control[1]
                if control[2] is not None:
                    built_control['controlValue'] = control[2]
                built_controls.setComponentByPosition(idx, built_control)
            else:
                raise LDAPControlError('control must be a sequence of 3 elements: controlType, criticality (boolean) and controlValue (None if not provided)')

        return built_controls


def validate_assertion_value(schema, name, value, auto_escape, auto_encode, validator, check_names):
    value = to_unicode(value)
    if auto_escape:
        if '\\' in value and not is_filter_escaped(value):
            value = escape_filter_chars(value)
    value = validate_attribute_value(schema, name, value, auto_encode, validator=validator, check_names=check_names)
    return value


def validate_attribute_value(schema, name, value, auto_encode, validator=None, check_names=False):
    conf_classes_excluded_from_check = [ v.lower() for v in get_config_parameter('CLASSES_EXCLUDED_FROM_CHECK') ]
    conf_attributes_excluded_from_check = [ v.lower() for v in get_config_parameter('ATTRIBUTES_EXCLUDED_FROM_CHECK') ]
    conf_utf8_syntaxes = get_config_parameter('UTF8_ENCODED_SYNTAXES')
    conf_utf8_types = [ v.lower() for v in get_config_parameter('UTF8_ENCODED_TYPES') ]
    if schema and schema.attribute_types:
        if ';' in name:
            name = name.split(';')[0]
        if check_names and schema.object_classes and name.lower() == 'objectclass':
            if to_unicode(value).lower() not in conf_classes_excluded_from_check and to_unicode(value) not in schema.object_classes:
                raise LDAPObjectClassError('invalid class in objectClass attribute: ' + str(value))
        elif check_names and name not in schema.attribute_types and name.lower() not in conf_attributes_excluded_from_check:
            raise LDAPAttributeError('invalid attribute ' + name)
        else:
            validator = find_attribute_validator(schema, name, validator)
            validated = validator(value)
            if validated is False:
                try:
                    if value[0:2] == "b'" and value[(-1)] == "'":
                        value = to_raw(value[2:-1])
                        validated = validator(value)
                except Exception:
                    raise LDAPInvalidValueError("value '%s' non valid for attribute '%s'" % (value, name))

            if validated is False:
                raise LDAPInvalidValueError("value '%s' non valid for attribute '%s'" % (value, name))
            elif validated is not True:
                value = validated
        if auto_encode and (name in schema.attribute_types and schema.attribute_types[name].syntax in conf_utf8_syntaxes or name.lower() in conf_utf8_types):
            value = to_unicode(value)
    return to_raw(value)


def prepare_filter_for_sending(raw_string):
    i = 0
    ints = []
    raw_string = to_raw(raw_string)
    while i < len(raw_string):
        if (raw_string[i] == 92 or raw_string[i] == '\\') and i < len(raw_string) - 2:
            try:
                ints.append(int(raw_string[i + 1:i + 3], 16))
                i += 2
            except ValueError:
                ints.append(92)

        elif str is not bytes:
            ints.append(raw_string[i])
        else:
            ints.append(ord(raw_string[i]))
        i += 1

    if str is not bytes:
        return bytes(ints)
    else:
        return ('').join(chr(x) for x in ints)


def prepare_for_sending(raw_string):
    if isinstance(raw_string, STRING_TYPES):
        return to_raw(raw_string)
    return raw_string