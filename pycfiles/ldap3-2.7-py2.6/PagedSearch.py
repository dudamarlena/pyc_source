# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\standard\PagedSearch.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ... import SUBTREE, DEREF_ALWAYS
from ...utils.dn import safe_dn
from ...core.results import DO_NOT_RAISE_EXCEPTIONS, RESULT_SIZE_LIMIT_EXCEEDED
from ...core.exceptions import LDAPOperationResult
from ...utils.log import log, log_enabled, ERROR, BASIC, PROTOCOL, NETWORK, EXTENDED

def paged_search_generator(connection, search_base, search_filter, search_scope=SUBTREE, dereference_aliases=DEREF_ALWAYS, attributes=None, size_limit=0, time_limit=0, types_only=False, get_operational_attributes=False, controls=None, paged_size=100, paged_criticality=False):
    if connection.check_names and search_base:
        search_base = safe_dn(search_base)
    responses = []
    original_connection = None
    original_auto_referrals = connection.auto_referrals
    connection.auto_referrals = False
    cookie = True
    cachekey = None
    while cookie:
        result = connection.search(search_base, search_filter, search_scope, dereference_aliases, attributes, size_limit, time_limit, types_only, get_operational_attributes, controls, paged_size, paged_criticality, None if cookie is True else cookie)
        if not isinstance(result, bool):
            (response, result) = connection.get_response(result)
        else:
            response = connection.response
            result = connection.result
        if result['referrals'] and original_auto_referrals:
            if not original_connection:
                original_connection = connection
            (_, connection, cachekey) = connection.strategy.create_referral_connection(result['referrals'])
            continue
        responses.extend(response)
        try:
            cookie = result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
        except KeyError:
            cookie = None

        if connection.raise_exceptions and result and result['result'] not in DO_NOT_RAISE_EXCEPTIONS:
            if log_enabled(PROTOCOL):
                log(PROTOCOL, 'paged search operation result <%s> for <%s>', result, connection)
            if result['result'] == RESULT_SIZE_LIMIT_EXCEEDED:
                while responses:
                    yield responses.pop()

            raise LDAPOperationResult(result=result['result'], description=result['description'], dn=result['dn'], message=result['message'], response_type=result['type'])
        while responses:
            yield responses.pop()

    if original_connection:
        connection = original_connection
        if connection.use_referral_cache and cachekey:
            connection.strategy.referral_cache[cachekey] = connection
        else:
            connection.unbind()
    connection.auto_referrals = original_auto_referrals
    connection.response = None
    return


def paged_search_accumulator(connection, search_base, search_filter, search_scope=SUBTREE, dereference_aliases=DEREF_ALWAYS, attributes=None, size_limit=0, time_limit=0, types_only=False, get_operational_attributes=False, controls=None, paged_size=100, paged_criticality=False):
    if connection.check_names and search_base:
        search_base = safe_dn(search_base)
    responses = []
    for response in paged_search_generator(connection, search_base, search_filter, search_scope, dereference_aliases, attributes, size_limit, time_limit, types_only, get_operational_attributes, controls, paged_size, paged_criticality):
        responses.append(response)

    connection.response = responses
    return responses