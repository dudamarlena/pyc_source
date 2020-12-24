# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\operation.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from ..core.results import RESULT_SUCCESS
from ..core.exceptions import LDAPExtensionError
from ..utils.asn1 import decoder

class ExtendedOperation(object):

    def __init__(self, connection, controls=None):
        self.connection = connection
        self.decoded_response = None
        self.result = None
        self.asn1_spec = None
        self.request_name = None
        self.response_name = None
        self.request_value = None
        self.response_value = None
        self.response_attribute = None
        self.controls = controls
        self.config()
        return

    def send(self):
        if self.connection.check_names:
            if self.connection.server.info is not None and self.connection.server.info.supported_extensions is not None:
                for request_name in self.connection.server.info.supported_extensions:
                    if request_name[0] == self.request_name:
                        break
                else:
                    raise LDAPExtensionError('extension not in DSA list of supported extensions')
            resp = self.connection.extended(self.request_name, self.request_value, self.controls)
            (_, self.result) = self.connection.strategy.sync or self.connection.get_response(resp)
        else:
            self.result = self.connection.result
        self.decode_response()
        self.populate_result()
        self.set_response()
        return self.response_value

    def populate_result(self):
        pass

    def decode_response(self):
        if not self.result:
            return
        else:
            if self.result['result'] not in [RESULT_SUCCESS]:
                if self.connection.raise_exceptions:
                    raise LDAPExtensionError('extended operation error: ' + self.result['description'] + ' - ' + self.result['message'])
                else:
                    return
            if not self.response_name or self.result['responseName'] == self.response_name:
                if self.result['responseValue']:
                    if self.asn1_spec is not None:
                        (decoded, unprocessed) = decoder.decode(self.result['responseValue'], asn1Spec=self.asn1_spec)
                        if unprocessed:
                            raise LDAPExtensionError('error decoding extended response value')
                        self.decoded_response = decoded
                    else:
                        self.decoded_response = self.result['responseValue']
            else:
                raise LDAPExtensionError('invalid response name received')
            return

    def set_response(self):
        self.response_value = self.result[self.response_attribute] if self.result and self.response_attribute in self.result else None
        self.connection.response = self.response_value
        return

    def config(self):
        pass