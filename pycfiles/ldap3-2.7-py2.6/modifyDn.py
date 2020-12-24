# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\modifyDn.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from ..protocol.rfc4511 import ModifyDNRequest, LDAPDN, RelativeLDAPDN, DeleteOldRDN, NewSuperior, ResultCode
from ..operation.bind import referrals_to_list

def modify_dn_operation(dn, new_relative_dn, delete_old_rdn=True, new_superior=None):
    request = ModifyDNRequest()
    request['entry'] = LDAPDN(dn)
    request['newrdn'] = RelativeLDAPDN(new_relative_dn)
    request['deleteoldrdn'] = DeleteOldRDN(delete_old_rdn)
    if new_superior:
        request['newSuperior'] = NewSuperior(new_superior)
    return request


def modify_dn_request_to_dict(request):
    return {'entry': str(request['entry']), 'newRdn': str(request['newrdn']), 
       'deleteOldRdn': bool(request['deleteoldrdn']), 
       'newSuperior': str(request['newSuperior']) if request['newSuperior'] is not None and request['newSuperior'].hasValue() else None}


def modify_dn_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'dn': str(response['matchedDN']), 
       'referrals': referrals_to_list(response['referral']), 
       'message': str(response['diagnosticMessage'])}