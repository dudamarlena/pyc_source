# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\strategy\sync.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
import socket
from .. import SEQUENCE_TYPES, get_config_parameter
from ..core.exceptions import LDAPSocketReceiveError, communication_exception_factory, LDAPExceptionError, LDAPExtensionError, LDAPOperationResult
from ..strategy.base import BaseStrategy, SESSION_TERMINATED_BY_SERVER, RESPONSE_COMPLETE, TRANSACTION_ERROR
from ..protocol.rfc4511 import LDAPMessage
from ..utils.log import log, log_enabled, ERROR, NETWORK, EXTENDED, format_ldap_message
from ..utils.asn1 import decoder, decode_message_fast
LDAP_MESSAGE_TEMPLATE = LDAPMessage()

class SyncStrategy(BaseStrategy):
    """
    This strategy is synchronous. You send the request and get the response
    Requests return a boolean value to indicate the result of the requested Operation
    Connection.response will contain the whole LDAP response for the messageId requested in a dict form
    Connection.request will contain the result LDAP message in a dict form
    """

    def __init__(self, ldap_connection):
        BaseStrategy.__init__(self, ldap_connection)
        self.sync = True
        self.no_real_dsa = False
        self.pooled = False
        self.can_stream = False
        self.socket_size = get_config_parameter('SOCKET_SIZE')

    def open(self, reset_usage=True, read_server_info=True):
        BaseStrategy.open(self, reset_usage, read_server_info)
        if read_server_info:
            try:
                self.connection.refresh_server_info()
            except LDAPOperationResult:
                self.connection.server._dsa_info = None
                self.connection.server._schema_info = None

        return

    def _start_listen(self):
        if not self.connection.listening and not self.connection.closed:
            self.connection.listening = True

    def receiving(self):
        """
        Receives data over the socket
        Checks if the socket is closed
        """
        messages = []
        receiving = True
        unprocessed = ''
        data = ''
        get_more_data = True
        exc = None
        while receiving:
            if get_more_data:
                try:
                    data = self.connection.socket.recv(self.socket_size)
                except (OSError, socket.error, AttributeError), e:
                    self.connection.last_error = 'error receiving data: ' + str(e)
                    try:
                        self.close()
                    except (socket.error, LDAPExceptionError):
                        pass
                    else:
                        if log_enabled(ERROR):
                            log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
                        raise communication_exception_factory(LDAPSocketReceiveError, type(e)(str(e)))(self.connection.last_error)
                else:
                    unprocessed += data
            if len(data) > 0:
                length = BaseStrategy.compute_ldap_message_size(unprocessed)
                if length == -1:
                    get_more_data = True
                    continue
                if len(unprocessed) < length:
                    get_more_data = True
                else:
                    if log_enabled(NETWORK):
                        log(NETWORK, 'received %d bytes via <%s>', len(unprocessed[:length]), self.connection)
                    messages.append(unprocessed[:length])
                    unprocessed = unprocessed[length:]
                    get_more_data = False
                    if len(unprocessed) == 0:
                        receiving = False
            else:
                receiving = False

        if log_enabled(NETWORK):
            log(NETWORK, 'received %d ldap messages via <%s>', len(messages), self.connection)
        return messages

    def post_send_single_response(self, message_id):
        """
        Executed after an Operation Request (except Search)
        Returns the result message or None
        """
        (responses, result) = self.get_response(message_id)
        self.connection.result = result
        if result['type'] == 'intermediateResponse':
            for response in responses:
                if response['type'] != 'intermediateResponse':
                    self.connection.last_error = 'multiple messages received error'
                    if log_enabled(ERROR):
                        log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
                    raise LDAPSocketReceiveError(self.connection.last_error)

        responses.append(result)
        return responses

    def post_send_search(self, message_id):
        """
        Executed after a search request
        Returns the result message and store in connection.response the objects found
        """
        (responses, result) = self.get_response(message_id)
        self.connection.result = result
        if isinstance(responses, SEQUENCE_TYPES):
            self.connection.response = responses[:]
            return responses
        self.connection.last_error = 'error receiving response'
        if log_enabled(ERROR):
            log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
        raise LDAPSocketReceiveError(self.connection.last_error)

    def _get_response(self, message_id, timeout):
        """
        Performs the capture of LDAP response for SyncStrategy
        """
        ldap_responses = []
        response_complete = False
        while not response_complete:
            responses = self.receiving()
            if responses:
                for response in responses:
                    if len(response) > 0:
                        if self.connection.usage:
                            self.connection._usage.update_received_message(len(response))
                        if self.connection.fast_decoder:
                            ldap_resp = decode_message_fast(response)
                            dict_response = self.decode_response_fast(ldap_resp)
                        else:
                            (ldap_resp, _) = decoder.decode(response, asn1Spec=LDAP_MESSAGE_TEMPLATE)
                            dict_response = self.decode_response(ldap_resp)
                        if log_enabled(EXTENDED):
                            log(EXTENDED, 'ldap message received via <%s>:%s', self.connection, format_ldap_message(ldap_resp, '<<'))
                        if int(ldap_resp['messageID']) == message_id:
                            ldap_responses.append(dict_response)
                            if dict_response['type'] not in ('searchResEntry', 'searchResRef',
                                                             'intermediateResponse'):
                                response_complete = True
                        elif int(ldap_resp['messageID']) == 0:
                            if dict_response['responseName'] == '1.3.6.1.4.1.1466.20036':
                                return SESSION_TERMINATED_BY_SERVER
                            if dict_response['responseName'] == '2.16.840.1.113719.1.27.103.4':
                                return TRANSACTION_ERROR
                            self.connection.last_error = 'unknown unsolicited notification from server'
                            if log_enabled(ERROR):
                                log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
                            raise LDAPSocketReceiveError(self.connection.last_error)
                        elif int(ldap_resp['messageID']) != message_id and dict_response['type'] == 'extendedResp':
                            self.connection.last_error = 'multiple extended responses to a single extended request'
                            if log_enabled(ERROR):
                                log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
                            raise LDAPExtensionError(self.connection.last_error)
                        else:
                            self.connection.last_error = 'invalid messageId received'
                            if log_enabled(ERROR):
                                log(ERROR, '<%s> for <%s>', self.connection.last_error, self.connection)
                            raise LDAPSocketReceiveError(self.connection.last_error)

            else:
                return SESSION_TERMINATED_BY_SERVER

        ldap_responses.append(RESPONSE_COMPLETE)
        return ldap_responses

    def set_stream(self, value):
        raise NotImplementedError

    def get_stream(self):
        raise NotImplementedError