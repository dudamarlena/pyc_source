# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\modify.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from .. import SEQUENCE_TYPES, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_INCREMENT
from ..protocol.rfc4511 import ModifyRequest, LDAPDN, Changes, Change, Operation, PartialAttribute, AttributeDescription, Vals, ResultCode
from ..operation.bind import referrals_to_list
from ..protocol.convert import changes_to_list, validate_attribute_value, prepare_for_sending
change_table = {MODIFY_ADD: 0, MODIFY_DELETE: 1, 
   MODIFY_REPLACE: 2, 
   MODIFY_INCREMENT: 3, 
   0: 0, 
   1: 1, 
   2: 2, 
   3: 3}

def modify_operation(dn, changes, auto_encode, schema=None, validator=None, check_names=False):
    change_list = Changes()
    pos = 0
    for attribute in changes:
        for change_operation in changes[attribute]:
            partial_attribute = PartialAttribute()
            partial_attribute['type'] = AttributeDescription(attribute)
            partial_attribute['vals'] = Vals()
            if isinstance(change_operation[1], SEQUENCE_TYPES):
                for (index, value) in enumerate(change_operation[1]):
                    partial_attribute['vals'].setComponentByPosition(index, prepare_for_sending(validate_attribute_value(schema, attribute, value, auto_encode, validator, check_names=check_names)))

            else:
                partial_attribute['vals'].setComponentByPosition(0, prepare_for_sending(validate_attribute_value(schema, attribute, change_operation[1], auto_encode, validator, check_names=check_names)))
            change = Change()
            change['operation'] = Operation(change_table[change_operation[0]])
            change['modification'] = partial_attribute
            change_list[pos] = change
            pos += 1

    request = ModifyRequest()
    request['object'] = LDAPDN(dn)
    request['changes'] = change_list
    return request


def modify_request_to_dict(request):
    return {'entry': str(request['object']), 'changes': changes_to_list(request['changes'])}


def modify_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'message': str(response['diagnosticMessage']), 
       'dn': str(response['matchedDN']), 
       'referrals': referrals_to_list(response['referral'])}