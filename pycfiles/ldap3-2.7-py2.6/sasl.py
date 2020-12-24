# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\sasl\sasl.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
import stringprep
from unicodedata import ucd_3_2_0 as unicode32
from os import urandom
from binascii import hexlify
from ... import SASL
from ...core.results import RESULT_AUTH_METHOD_NOT_SUPPORTED
from ...core.exceptions import LDAPSASLPrepError, LDAPPasswordIsMandatoryError

def sasl_prep(data):
    """
    implement SASLPrep profile as per RFC4013:
    it defines the "SASLprep" profile of the "stringprep" algorithm [StringPrep].
    The profile is designed for use in Simple Authentication and Security
    Layer ([SASL]) mechanisms, such as [PLAIN], [CRAM-MD5], and
    [DIGEST-MD5].  It may be applicable where simple user names and
    passwords are used.  This profile is not intended for use in
    preparing identity strings that are not simple user names (e.g.,
    email addresses, domain names, distinguished names), or where
    identity or password strings that are not character data, or require
    different handling (e.g., case folding).
    """
    prepared_data = ''
    for c in data:
        if stringprep.in_table_c12(c):
            prepared_data += ' '
        elif stringprep.in_table_b1(c):
            pass
        else:
            prepared_data += c

    prepared_data = unicode32.normalize('NFKC', prepared_data)
    if not prepared_data:
        raise LDAPSASLPrepError('SASLprep error: unable to normalize string')
    for c in prepared_data:
        if stringprep.in_table_c12(c):
            raise LDAPSASLPrepError('SASLprep error: non-ASCII space character present')
        elif stringprep.in_table_c21(c):
            raise LDAPSASLPrepError('SASLprep error: ASCII control character present')
        elif stringprep.in_table_c22(c):
            raise LDAPSASLPrepError('SASLprep error: non-ASCII control character present')
        elif stringprep.in_table_c3(c):
            raise LDAPSASLPrepError('SASLprep error: private character present')
        elif stringprep.in_table_c4(c):
            raise LDAPSASLPrepError('SASLprep error: non-character code point present')
        elif stringprep.in_table_c5(c):
            raise LDAPSASLPrepError('SASLprep error: surrogate code point present')
        elif stringprep.in_table_c6(c):
            raise LDAPSASLPrepError('SASLprep error: inappropriate for plain text character present')
        elif stringprep.in_table_c7(c):
            raise LDAPSASLPrepError('SASLprep error: inappropriate for canonical representation character present')
        elif stringprep.in_table_c8(c):
            raise LDAPSASLPrepError('SASLprep error: change display property or deprecated character present')
        elif stringprep.in_table_c9(c):
            raise LDAPSASLPrepError('SASLprep error: tagging character present')

    flag_r_and_al_cat = False
    flag_l_cat = False
    for c in prepared_data:
        if stringprep.in_table_d1(c):
            flag_r_and_al_cat = True
        elif stringprep.in_table_d2(c):
            flag_l_cat = True
        if flag_r_and_al_cat and flag_l_cat:
            raise LDAPSASLPrepError('SASLprep error: string cannot contain (R or AL) and L bidirectional chars')

    if flag_r_and_al_cat and not stringprep.in_table_d1(prepared_data[0]) and not stringprep.in_table_d2(prepared_data[(-1)]):
        raise LDAPSASLPrepError('r_and_al_cat character present, must be first and last character of the string')
    return prepared_data


def validate_simple_password(password, accept_empty=False):
    """
    validate simple password as per RFC4013 using sasl_prep:
    """
    if accept_empty and not password:
        return password
    if not password:
        raise LDAPPasswordIsMandatoryError("simple password can't be empty")
    if not isinstance(password, bytes):
        password = sasl_prep(password)
        if not isinstance(password, bytes):
            password = password.encode('utf-8')
    return password


def abort_sasl_negotiation(connection, controls):
    from ...operation.bind import bind_operation
    request = bind_operation(connection.version, SASL, None, None, '', None)
    response = connection.post_send_single_response(connection.send('bindRequest', request, controls))
    if connection.strategy.sync:
        result = connection.result
    else:
        result = connection.get_response(response)[0][0]
    if result['result'] == RESULT_AUTH_METHOD_NOT_SUPPORTED:
        return True
    else:
        return False


def send_sasl_negotiation(connection, controls, payload):
    from ...operation.bind import bind_operation
    request = bind_operation(connection.version, SASL, None, None, connection.sasl_mechanism, payload)
    response = connection.post_send_single_response(connection.send('bindRequest', request, controls))
    if connection.strategy.sync:
        result = connection.result
    else:
        (_, result) = connection.get_response(response)
    return result


def random_hex_string(size):
    return str(hexlify(urandom(size)).decode('ascii'))