# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\delete.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ..protocol.rfc4511 import DelRequest, LDAPDN, ResultCode
from ..operation.bind import referrals_to_list

def delete_operation(dn):
    request = DelRequest(LDAPDN(dn))
    return request


def delete_request_to_dict(request):
    return {'entry': str(request)}


def delete_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'dn': str(response['matchedDN']), 
       'message': str(response['diagnosticMessage']), 
       'referrals': referrals_to_list(response['referral'])}