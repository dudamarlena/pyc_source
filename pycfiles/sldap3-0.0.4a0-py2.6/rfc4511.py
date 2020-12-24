# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\protocol\rfc4511.py
# Compiled at: 2015-04-21 11:26:07
"""
"""
from ldap3.protocol.rfc4511 import LDAPResult, LDAPMessage, ProtocolOp, MessageID, Referral, BindResponse, ServerSaslCreds, ExtendedResponse
from ldap3.protocol.convert import build_controls_list

def build_ldap_message(message_id, response_type, response, controls=None):
    ldap_message = LDAPMessage()
    ldap_message['messageID'] = MessageID(message_id)
    ldap_message['protocolOp'] = ProtocolOp().setComponentByName(response_type, response)
    message_controls = build_controls_list(controls)
    if message_controls is not None:
        ldap_message['controls'] = message_controls
    return ldap_message


def build_ldap_result(result_code, matched_dn='', diagnostic_message='', referral=None):
    ldap_result = LDAPResult()
    ldap_result['resultCode'] = result_code
    ldap_result['matchedDN'] = matched_dn
    ldap_result['diagnosticMessage'] = diagnostic_message
    if referral:
        ldap_result['referral'] = Referral(referral)
    return ldap_result


def build_bind_response(ldap_result, server_sasl_credentials):
    response = BindResponse()
    response['resultCode'] = ldap_result['resultCode']
    response['matchedDN'] = ldap_result['matchedDN']
    response['diagnosticMessage'] = ldap_result['diagnosticMessage']
    if ldap_result['referral']:
        response['referral'] = ldap_result['referral']
    if server_sasl_credentials:
        response['serverSaslCreds'] = ServerSaslCreds(server_sasl_credentials)
    return response


def build_extended_response(ldap_result, response_name=None, response_value=None):
    response = ExtendedResponse()
    response['resultCode'] = ldap_result['resultCode']
    response['matchedDN'] = ldap_result['matchedDN']
    response['diagnosticMessage'] = ldap_result['diagnosticMessage']
    if response_name:
        response['responseName'] = response_name
    if response_value:
        response['responseValue'] = response_value
    return response