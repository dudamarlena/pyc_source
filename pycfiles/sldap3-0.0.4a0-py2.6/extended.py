# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\operation\extended.py
# Compiled at: 2015-04-22 17:42:46
"""
"""
import logging
from .. import NATIVE_ASYNCIO
if NATIVE_ASYNCIO:
    import asyncio
else:
    import trollius as asyncio
    from trollius import From, Return
from ldap3 import RESULT_SUCCESS, RESULT_PROTOCOL_ERROR, RESULT_UNAVAILABLE
from ..protocol.rfc4511 import build_ldap_result, build_extended_response

@asyncio.coroutine
def do_extended_operation(dua, message_id, dict_req):
    logging.debug('do EXTENDED operation for DUA %s: %s' % (dua.identity, str(dict_req)))
    if dict_req['name'] == '1.3.6.1.4.1.1466.20037':
        if dua.dsa.secure_port:
            result = build_ldap_result(RESULT_SUCCESS)
        else:
            result = build_ldap_result(RESULT_UNAVAILABLE)
        response = build_extended_response(result, '1.3.6.1.4.1.1466.20037')
    else:
        result = build_ldap_result(RESULT_PROTOCOL_ERROR, diagnostic_message='extended operation not supported')
        response = build_extended_response(result)
    if NATIVE_ASYNCIO:
        return (response, 'extendedResp')
    raise Response((response, 'extendedRespo'))