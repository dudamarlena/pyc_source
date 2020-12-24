# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\microsoft\unlockAccount.py
# Compiled at: 2020-02-23 02:04:03
"""
"""
from ... import MODIFY_REPLACE
from ...utils.log import log, log_enabled, PROTOCOL
from ...core.results import RESULT_SUCCESS
from ...utils.dn import safe_dn

def ad_unlock_account(connection, user_dn, controls=None):
    if connection.check_names:
        user_dn = safe_dn(user_dn)
    result = connection.modify(user_dn, {'lockoutTime': [(MODIFY_REPLACE, ['0'])]}, controls)
    if not connection.strategy.sync:
        (_, result) = connection.get_response(result)
    else:
        result = connection.result
    if result['result'] == RESULT_SUCCESS:
        return True
    if connection.raise_exceptions:
        from ...core.exceptions import LDAPOperationResult
        if log_enabled(PROTOCOL):
            log(PROTOCOL, 'operation result <%s> for <%s>', result, connection)
        raise LDAPOperationResult(result=result['result'], description=result['description'], dn=result['dn'], message=result['message'], response_type=result['type'])
    return result