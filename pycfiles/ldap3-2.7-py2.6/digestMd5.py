# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\sasl\digestMd5.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from binascii import hexlify
import hashlib, hmac
from ... import SEQUENCE_TYPES
from ...protocol.sasl.sasl import abort_sasl_negotiation, send_sasl_negotiation, random_hex_string
STATE_KEY = 0
STATE_VALUE = 1

def md5_h(value):
    if not isinstance(value, bytes):
        value = value.encode()
    return hashlib.md5(value).digest()


def md5_kd(k, s):
    if not isinstance(k, bytes):
        k = k.encode()
    if not isinstance(s, bytes):
        s = s.encode()
    return md5_h(k + ':' + s)


def md5_hex(value):
    if not isinstance(value, bytes):
        value = value.encode()
    return hexlify(value)


def md5_hmac(k, s):
    if not isinstance(k, bytes):
        k = k.encode()
    if not isinstance(s, bytes):
        s = s.encode()
    return hmac.new(k, s, digestmod=hashlib.md5).hexdigest()


def sasl_digest_md5(connection, controls):
    if not isinstance(connection.sasl_credentials, SEQUENCE_TYPES) or not len(connection.sasl_credentials) == 4:
        return
    else:
        result = send_sasl_negotiation(connection, controls, None)
        if 'saslCreds' in result and result['saslCreds'] is not None:
            server_directives = decode_directives(result['saslCreds'])
        else:
            return
        if 'realm' not in server_directives or 'nonce' not in server_directives or 'algorithm' not in server_directives:
            abort_sasl_negotiation(connection, controls)
            return
        charset = server_directives['charset'] if 'charset' in server_directives and server_directives['charset'].lower() == 'utf-8' else 'iso8859-1'
        user = connection.sasl_credentials[1].encode(charset)
        realm = connection.sasl_credentials[0] if connection.sasl_credentials[0] else server_directives['realm'] if ('realm' in server_directives) else ''.encode(charset)
        password = connection.sasl_credentials[2].encode(charset)
        authz_id = connection.sasl_credentials[3].encode(charset) if connection.sasl_credentials[3] else ''
        nonce = server_directives['nonce'].encode(charset)
        cnonce = random_hex_string(16).encode(charset)
        uri = 'ldap/'
        qop = 'auth'
        digest_response = 'username="' + user + '",'
        digest_response += 'realm="' + realm + '",'
        digest_response += 'authzid="' + authz_id + '",' if authz_id else ''
        digest_response += 'nonce="' + nonce + '",'
        digest_response += 'cnonce="' + cnonce + '",'
        digest_response += 'digest-uri="' + uri + '",'
        digest_response += 'qop=' + qop + ','
        digest_response += 'nc=00000001,'
        if charset == 'utf-8':
            digest_response += 'charset="utf-8",'
        a0 = md5_h((':').join([user, realm, password]))
        a1 = (':').join([a0, nonce, cnonce, authz_id]) if authz_id else (':').join([a0, nonce, cnonce])
        a2 = 'AUTHENTICATE:' + uri + (':00000000000000000000000000000000' if qop in ('auth-int',
                                                                                     'auth-conf') else '')
        digest_response += 'response="' + md5_hex(md5_kd(md5_hex(md5_h(a1)), (':').join([nonce, '00000001', cnonce, qop, md5_hex(md5_h(a2))]))) + '"'
        result = send_sasl_negotiation(connection, controls, digest_response)
        return result


def decode_directives(directives_string):
    """
    converts directives to dict, unquote values
    """
    state = STATE_KEY
    tmp_buffer = ''
    quoting = False
    key = ''
    directives = dict()
    for c in directives_string.decode('utf-8'):
        if state == STATE_KEY and c == '=':
            key = tmp_buffer
            tmp_buffer = ''
            state = STATE_VALUE
        elif state == STATE_VALUE and c == '"' and not quoting and not tmp_buffer:
            quoting = True
        elif state == STATE_VALUE and c == '"' and quoting:
            quoting = False
        elif state == STATE_VALUE and c == ',' and not quoting:
            directives[key] = tmp_buffer
            tmp_buffer = ''
            key = ''
            state = STATE_KEY
        else:
            tmp_buffer += c

    if key and tmp_buffer:
        directives[key] = tmp_buffer
    return directives