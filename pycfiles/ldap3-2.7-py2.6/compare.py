# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\compare.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from ..protocol.convert import validate_attribute_value, prepare_for_sending
from ..protocol.rfc4511 import CompareRequest, AttributeValueAssertion, AttributeDescription, LDAPDN, AssertionValue, ResultCode
from ..operation.search import ava_to_dict
from ..operation.bind import referrals_to_list

def compare_operation(dn, attribute, value, auto_encode, schema=None, validator=None, check_names=False):
    ava = AttributeValueAssertion()
    ava['attributeDesc'] = AttributeDescription(attribute)
    ava['assertionValue'] = AssertionValue(prepare_for_sending(validate_attribute_value(schema, attribute, value, auto_encode, validator, check_names=check_names)))
    request = CompareRequest()
    request['entry'] = LDAPDN(dn)
    request['ava'] = ava
    return request


def compare_request_to_dict(request):
    ava = ava_to_dict(request['ava'])
    return {'entry': str(request['entry']), 'attribute': ava['attribute'], 
       'value': ava['value']}


def compare_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'dn': str(response['matchedDN']), 
       'message': str(response['diagnosticMessage']), 'referrals': referrals_to_list(response['referral'])}