# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\extended.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from pyasn1.type.univ import OctetString
from pyasn1.type.base import Asn1Item
from ..core.results import RESULT_CODES
from ..protocol.rfc4511 import ExtendedRequest, RequestName, ResultCode, RequestValue
from ..protocol.convert import referrals_to_list
from ..utils.asn1 import encode
from ..utils.conv import to_unicode

def extended_operation(request_name, request_value=None, no_encode=None):
    request = ExtendedRequest()
    request['requestName'] = RequestName(request_name)
    if request_value and isinstance(request_value, Asn1Item):
        request['requestValue'] = RequestValue(encode(request_value))
    elif str is not bytes and isinstance(request_value, (bytes, bytearray)):
        request['requestValue'] = request_value
    elif request_value and no_encode:
        request['requestValue'] = request_value
    elif request_value:
        request['requestValue'] = RequestValue(encode(OctetString(str(request_value))))
    return request


def extended_request_to_dict(request):
    return {'name': str(request['requestName']), 'value': bytes(request['requestValue']) if 'requestValue' in request and request['requestValue'] is not None and request['requestValue'].hasValue() else None}


def extended_response_to_dict(response):
    return {'result': int(response['resultCode']), 'dn': str(response['matchedDN']), 
       'message': str(response['diagnosticMessage']), 
       'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'referrals': referrals_to_list(response['referral']), 
       'responseName': str(response['responseName']) if response['responseName'] is not None and response['responseName'].hasValue() else str(), 
       'responseValue': bytes(response['responseValue']) if response['responseValue'] is not None and response['responseValue'].hasValue() else bytes()}


def intermediate_response_to_dict(response):
    return {'responseName': str(response['responseName']), 'responseValue': bytes(response['responseValue']) if response['responseValue'] else bytes()}


def extended_response_to_dict_fast(response):
    response_dict = dict()
    response_dict['result'] = int(response[0][3])
    response_dict['description'] = RESULT_CODES[response_dict['result']]
    response_dict['dn'] = to_unicode(response[1][3], from_server=True)
    response_dict['message'] = to_unicode(response[2][3], from_server=True)
    response_dict['referrals'] = None
    response_dict['responseName'] = None
    response_dict['responseValue'] = None
    for r in response[3:]:
        if r[2] == 3:
            response_dict['referrals'] = referrals_to_list(r[3])
        elif r[2] == 10:
            response_dict['responseName'] = to_unicode(r[3], from_server=True)
            response_dict['responseValue'] = ''
        else:
            response_dict['responseValue'] = bytes(r[3])

    return response_dict


def intermediate_response_to_dict_fast(response):
    response_dict = dict()
    for r in response:
        if r[2] == 0:
            response_dict['responseName'] = to_unicode(r[3], from_server=True)
        else:
            response_dict['responseValue'] = bytes(r[3])

    return response_dict