# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/wtdojo/wtdojo/validators.py
# Compiled at: 2014-12-11 07:55:59
"""
Module for translating WTForms validators to Dojo validation constraints
"""

def get_dojo_constraint(field, V):
    """
    Given a WTForms validator object, returns the dojo contraints string required to implement the same
    validator using Dojo
    """
    validator_type = V.__class__.__name__
    if 'Required' == validator_type:
        return ('property', 'required=True')
    else:
        return ('', '')


def get_dojo_constraints(field):
    """
    Given a list of WTForms validator objects, returns the dojo properties and constraints lists required to implement
    the same validators using Dojo
    """
    properties = []
    constraints = []
    dojo_properties = []
    for V in field.validators:
        vt, s = get_dojo_constraint(field, V)
        if '' != s:
            if 'property' == vt:
                properties.append(s)
            elif 'dojo_property' == vt:
                dojo_properties.append(s)
            elif 'constraint' == vt:
                constraints.append(s)

    return (
     properties, dojo_properties, constraints)


def get_validation_str(field):
    """
    Given a field, returns a string suitable for placing inside the
    <input> or <div> etc tags to actually implement the validation according to the field's validators
    """
    props_str = ''
    dojo_props_str = ''
    dojo_constraints_str = ''
    use_comma = ''
    if len(field.validators) > 0:
        properties, dojo_properties, constraints = get_dojo_constraints(field)
        if len(properties) > 0:
            props_str = (' ').join(properties)
        if len(dojo_properties) > 0:
            dojo_props_str = (', ').join(dojo_properties)
            use_comma = ','
        if len(constraints) > 0:
            dojo_constraints_str = (', ').join(constraints)
    return '%s data-dojo-props="%s%s constraints: {%s}"' % (props_str, dojo_props_str, use_comma, dojo_constraints_str)