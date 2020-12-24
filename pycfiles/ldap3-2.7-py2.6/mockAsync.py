# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\strategy\mockAsync.py
# Compiled at: 2020-02-23 02:04:03
"""
"""
from .. import ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, NO_ATTRIBUTES
from .mockBase import MockBaseStrategy
from .asynchronous import AsyncStrategy
from ..operation.search import search_result_done_response_to_dict, search_result_entry_response_to_dict
from ..core.results import DO_NOT_RAISE_EXCEPTIONS
from ..utils.log import log, log_enabled, ERROR, PROTOCOL
from ..core.exceptions import LDAPResponseTimeoutError, LDAPOperationResult
from ..operation.bind import bind_response_to_dict
from ..operation.delete import delete_response_to_dict
from ..operation.add import add_response_to_dict
from ..operation.compare import compare_response_to_dict
from ..operation.modifyDn import modify_dn_response_to_dict
from ..operation.modify import modify_response_to_dict
from ..operation.search import search_result_done_response_to_dict, search_result_entry_response_to_dict
from ..operation.extended import extended_response_to_dict

class MockAsyncStrategy(MockBaseStrategy, AsyncStrategy):
    """
    This strategy create a mock LDAP server, with asynchronous access
    It can be useful to test LDAP without accessing a real Server
    """

    def __init__(self, ldap_connection):
        AsyncStrategy.__init__(self, ldap_connection)
        MockBaseStrategy.__init__(self)

    def post_send_search(self, payload):
        (message_id, message_type, request, controls) = payload
        async_response = []
        async_result = dict()
        if message_type == 'searchRequest':
            (responses, result) = self.mock_search(request, controls)
            result['type'] = 'searchResDone'
            for entry in responses:
                response = search_result_entry_response_to_dict(entry, self.connection.server.schema, self.connection.server.custom_formatter, self.connection.check_names)
                response['type'] = 'searchResEntry'
                if self.connection.empty_attributes:
                    for attribute_type in request['attributes']:
                        attribute_name = str(attribute_type)
                        if attribute_name not in response['raw_attributes'] and attribute_name not in (ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, NO_ATTRIBUTES):
                            response['raw_attributes'][attribute_name] = list()
                            response['attributes'][attribute_name] = list()
                            if log_enabled(PROTOCOL):
                                log(PROTOCOL, 'attribute set to empty list for missing attribute <%s> in <%s>', attribute_type, self)

                    if not self.connection.auto_range:
                        attrs_to_remove = []
                        for attribute_type in response['attributes']:
                            attribute_name = str(attribute_type)
                            if ';range' in attribute_name.lower():
                                (orig_attr, _, _) = attribute_name.partition(';')
                                attrs_to_remove.append(orig_attr)

                        for attribute_type in attrs_to_remove:
                            if log_enabled(PROTOCOL):
                                log(PROTOCOL, 'attribute type <%s> removed in response because of same attribute returned as range by the server in <%s>', attribute_type, self)
                            del response['raw_attributes'][attribute_type]
                            del response['attributes'][attribute_type]

                async_response.append(response)

            async_result = search_result_done_response_to_dict(result)
            async_result['type'] = 'searchResDone'
        self._responses[message_id] = (
         request, async_result, async_response)
        return message_id

    def post_send_single_response(self, payload):
        (message_id, message_type, request, controls) = payload
        responses = []
        result = None
        if message_type == 'bindRequest':
            result = bind_response_to_dict(self.mock_bind(request, controls))
            result['type'] = 'bindResponse'
        elif message_type == 'unbindRequest':
            self.bound = None
        elif message_type == 'abandonRequest':
            pass
        elif message_type == 'delRequest':
            result = delete_response_to_dict(self.mock_delete(request, controls))
            result['type'] = 'delResponse'
        elif message_type == 'addRequest':
            result = add_response_to_dict(self.mock_add(request, controls))
            result['type'] = 'addResponse'
        elif message_type == 'compareRequest':
            result = compare_response_to_dict(self.mock_compare(request, controls))
            result['type'] = 'compareResponse'
        elif message_type == 'modDNRequest':
            result = modify_dn_response_to_dict(self.mock_modify_dn(request, controls))
            result['type'] = 'modDNResponse'
        elif message_type == 'modifyRequest':
            result = modify_response_to_dict(self.mock_modify(request, controls))
            result['type'] = 'modifyResponse'
        elif message_type == 'extendedReq':
            result = extended_response_to_dict(self.mock_extended(request, controls))
            result['type'] = 'extendedResp'
        responses.append(result)
        if self.connection.raise_exceptions and result and result['result'] not in DO_NOT_RAISE_EXCEPTIONS:
            if log_enabled(PROTOCOL):
                log(PROTOCOL, 'operation result <%s> for <%s>', result, self.connection)
            raise LDAPOperationResult(result=result['result'], description=result['description'], dn=result['dn'], message=result['message'], response_type=result['type'])
        self._responses[message_id] = (
         request, result, responses)
        return message_id

    def get_response(self, message_id, timeout=None, get_request=False):
        if message_id in self._responses:
            (request, result, response) = self._responses.pop(message_id)
        else:
            raise LDAPResponseTimeoutError('message id not in outstanding queue')
        if self.connection.raise_exceptions and result and result['result'] not in DO_NOT_RAISE_EXCEPTIONS:
            if log_enabled(PROTOCOL):
                log(PROTOCOL, 'operation result <%s> for <%s>', result, self.connection)
            raise LDAPOperationResult(result=result['result'], description=result['description'], dn=result['dn'], message=result['message'], response_type=result['type'])
        if get_request:
            return (response, result, request)
        else:
            return (
             response, result)