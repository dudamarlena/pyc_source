# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\operation\bind.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from .. import SIMPLE, ANONYMOUS, SASL, STRING_TYPES
from ..core.results import RESULT_CODES
from ..core.exceptions import LDAPUserNameIsMandatoryError, LDAPPasswordIsMandatoryError, LDAPUnknownAuthenticationMethodError, LDAPUserNameNotAllowedError
from ..protocol.sasl.sasl import validate_simple_password
from ..protocol.rfc4511 import Version, AuthenticationChoice, Simple, BindRequest, ResultCode, SaslCredentials, BindResponse, LDAPDN, LDAPString, Referral, ServerSaslCreds, SicilyPackageDiscovery, SicilyNegotiate, SicilyResponse
from ..protocol.convert import authentication_choice_to_dict, referrals_to_list
from ..utils.conv import to_unicode, to_raw

def bind_operation(version, authentication, name='', password=None, sasl_mechanism=None, sasl_credentials=None, auto_encode=False):
    request = BindRequest()
    request['version'] = Version(version)
    if name is None:
        name = ''
    if isinstance(name, STRING_TYPES):
        request['name'] = to_unicode(name) if auto_encode else name
    if authentication == SIMPLE:
        if not name:
            raise LDAPUserNameIsMandatoryError('user name is mandatory in simple bind')
        if password:
            request['authentication'] = AuthenticationChoice().setComponentByName('simple', Simple(validate_simple_password(password)))
        else:
            raise LDAPPasswordIsMandatoryError('password is mandatory in simple bind')
    elif authentication == SASL:
        sasl_creds = SaslCredentials()
        sasl_creds['mechanism'] = sasl_mechanism
        if sasl_credentials is not None:
            sasl_creds['credentials'] = sasl_credentials
        request['authentication'] = AuthenticationChoice().setComponentByName('sasl', sasl_creds)
    elif authentication == ANONYMOUS:
        if name:
            raise LDAPUserNameNotAllowedError('user name not allowed in anonymous bind')
        request['name'] = ''
        request['authentication'] = AuthenticationChoice().setComponentByName('simple', Simple(''))
    elif authentication == 'SICILY_PACKAGE_DISCOVERY':
        request['name'] = ''
        request['authentication'] = AuthenticationChoice().setComponentByName('sicilyPackageDiscovery', SicilyPackageDiscovery(''))
    elif authentication == 'SICILY_NEGOTIATE_NTLM':
        request['name'] = 'NTLM'
        request['authentication'] = AuthenticationChoice().setComponentByName('sicilyNegotiate', SicilyNegotiate(name.create_negotiate_message()))
    elif authentication == 'SICILY_RESPONSE_NTLM':
        name.parse_challenge_message(password)
        server_creds = name.create_authenticate_message()
        if server_creds:
            request['name'] = ''
            request['authentication'] = AuthenticationChoice().setComponentByName('sicilyResponse', SicilyResponse(server_creds))
        else:
            request = None
    else:
        raise LDAPUnknownAuthenticationMethodError('unknown authentication method')
    return request


def bind_request_to_dict(request):
    return {'version': int(request['version']), 'name': str(request['name']), 
       'authentication': authentication_choice_to_dict(request['authentication'])}


def bind_response_operation(result_code, matched_dn='', diagnostic_message='', referral=None, server_sasl_credentials=None):
    response = BindResponse()
    response['resultCode'] = ResultCode(result_code)
    response['matchedDN'] = LDAPDN(matched_dn)
    response['diagnosticMessage'] = LDAPString(diagnostic_message)
    if referral:
        response['referral'] = Referral(referral)
    if server_sasl_credentials:
        response['serverSaslCreds'] = ServerSaslCreds(server_sasl_credentials)
    return response


def bind_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'dn': str(response['matchedDN']), 
       'message': str(response['diagnosticMessage']), 
       'referrals': referrals_to_list(response['referral']) if response['referral'] is not None and response['referral'].hasValue() else [], 
       'saslCreds': bytes(response['serverSaslCreds']) if response['serverSaslCreds'] is not None and response['serverSaslCreds'].hasValue() else None}


def sicily_bind_response_to_dict(response):
    return {'result': int(response['resultCode']), 'description': ResultCode().getNamedValues().getName(response['resultCode']), 
       'server_creds': bytes(response['matchedDN']), 
       'error_message': str(response['diagnosticMessage'])}


def bind_response_to_dict_fast(response):
    response_dict = dict()
    response_dict['result'] = int(response[0][3])
    response_dict['description'] = RESULT_CODES[response_dict['result']]
    response_dict['dn'] = to_unicode(response[1][3], from_server=True)
    response_dict['message'] = to_unicode(response[2][3], from_server=True)
    response_dict['referrals'] = None
    response_dict['saslCreds'] = None
    for r in response[3:]:
        if r[2] == 3:
            response_dict['referrals'] = referrals_to_list(r[3])
        else:
            response_dict['saslCreds'] = bytes(r[3])

    return response_dict


def sicily_bind_response_to_dict_fast(response):
    response_dict = dict()
    response_dict['result'] = int(response[0][3])
    response_dict['description'] = RESULT_CODES[response_dict['result']]
    response_dict['server_creds'] = bytes(response[1][3])
    response_dict['error_message'] = to_unicode(response[2][3], from_server=True)
    return response_dict