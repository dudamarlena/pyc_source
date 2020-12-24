# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/opentea/noob/validate_light.py
# Compiled at: 2019-07-18 11:38:44
# Size of source mod 2**32: 2626 bytes
"""Lightweight validate from jsonschema"""
import jsonschema, numpy as np
from opentea.noob.noob import nob_pprint

class ValidationErrorShort(Exception):
    __doc__ = 'Valodation error'


def validate_light(data, schema):
    """Schema validation procedure.

    Parameters:
    -----------
    data : a nested dict to validate
    schema : the schema to validate against (jsonschema grammar)

    Return:
    -------
    THIS IS NOT A BOOLEAN
    Only exceptions are returned if any problem, else none."""
    err_msg = validate_base(data, schema)
    if err_msg:
        raise ValidationErrorShort(err_msg)


def validate_base(data, schema):
    """Validate in the default case ."""
    validator = jsonschema.Draft4Validator(schema)
    errors = sorted((validator.iter_errors(data)), key=(lambda e: e.path))
    err_msg = ''
    if errors:
        for error in errors:
            if 'oneOf' in error.schema:
                err_msg += validate_in_oneof(error.instance, error.schema)
            else:
                if error.schema['type'] == 'number':
                    if isinstance(error.instance, np.ndarray):
                        continue
                err_msg += '\n========================'
                err_msg += '\n' + nob_pprint(error.instance)
                err_msg += '\n does not validate against '
                err_msg += '\n' + nob_pprint((error.schema), max_lvl=4)

    return err_msg


def validate_in_oneof(data, schema):
    """Validate in the case on an opentea oneOf schema."""
    err_msg = ''
    l_keys = list(data.keys())
    if not l_keys:
        err_msg += '\n========================'
        err_msg += '\n' + nob_pprint(data)
        err_msg += '\nNo child found, cannot validate against a oneOf'
    else:
        if len(l_keys) > 1:
            err_msg += '\n========================'
            err_msg += '\n' + nob_pprint(data)
            err_msg += '\nSeveral child found, cannot validate against a oneOf'
        else:
            item = l_keys[0]
            oneof_list = list()
            for option in schema['oneOf']:
                oneof_list.append(option['required'][0])
                if item not in oneof_list:
                    err_msg += '\n========================'
                    err_msg += '\n' + item + ' not in ' + ' '.join(oneof_list)
                else:
                    idx = oneof_list.index(item)
                    err_msg = validate_base(data[item], schema['oneOf'][idx]['properties'][item])

    return err_msg