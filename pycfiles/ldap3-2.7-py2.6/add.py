# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\add.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from .. import SEQUENCE_TYPES
from ..protocol.rfc4511 import AddRequest, LDAPDN, AttributeList, Attribute, AttributeDescription, ResultCode, Vals
from ..protocol.convert import referrals_to_list, attributes_to_dict, validate_attribute_value, prepare_for_sending

def add_operation(dn, attributes, auto_encode, schema=None, validator=None, check_names=False):
    attribute_list = AttributeList()
    for (pos, attribute) in enumerate(attributes):
        attribute_list[pos] = Attribute()
        attribute_list[pos]['type'] = AttributeDescription(attribute)
        vals = Vals()
        if isinstance(attributes[attribute], SEQUENCE_TYPES):
            for (index, value) in enumerate(attributes[attribute]):
                vals.setComponentByPosition(index, prepare_for_sending(validate_attribute_value(schema, attribute, value, auto_encode, validator, check_names)))

        else:
            vals.setComponentByPosition(0, prepare_for_sending(validate_attribute_value(schema, attribute, attributes[attribute], auto_encode, validator, check_names)))
        attribute_list[pos]['vals'] = vals

    request = AddRequest()
    request['entry'] = LDAPDN(dn)
    request['attributes'] = attribute_list
    return request


def add_request_to_dict(request):
    return {'entry': str(request['entry']), 'attributes': attributes_to_dict(request['attributes'])}


def add_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'dn': str(response['matchedDN']), 
       'message': str(response['diagnosticMessage']), 
       'referrals': referrals_to_list(response['referral'])}