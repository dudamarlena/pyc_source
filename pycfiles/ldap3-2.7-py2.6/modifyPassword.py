# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\standard\modifyPassword.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from ... import HASHED_NONE
from ...extend.operation import ExtendedOperation
from ...protocol.rfc3062 import PasswdModifyRequestValue, PasswdModifyResponseValue
from ...utils.hashed import hashed
from ...protocol.sasl.sasl import validate_simple_password
from ...utils.dn import safe_dn
from ...core.results import RESULT_SUCCESS

class ModifyPassword(ExtendedOperation):

    def config(self):
        self.request_name = '1.3.6.1.4.1.4203.1.11.1'
        self.request_value = PasswdModifyRequestValue()
        self.asn1_spec = PasswdModifyResponseValue()
        self.response_attribute = 'new_password'

    def __init__(self, connection, user=None, old_password=None, new_password=None, hash_algorithm=None, salt=None, controls=None):
        ExtendedOperation.__init__(self, connection, controls)
        if user:
            if connection.check_names:
                user = safe_dn(user)
            self.request_value['userIdentity'] = user
        if old_password:
            if not isinstance(old_password, bytes):
                old_password = validate_simple_password(old_password, True)
            self.request_value['oldPasswd'] = old_password
        if new_password:
            if not isinstance(new_password, bytes):
                new_password = validate_simple_password(new_password, True)
            if hash_algorithm is None or hash_algorithm == HASHED_NONE:
                self.request_value['newPasswd'] = new_password
            else:
                self.request_value['newPasswd'] = hashed(hash_algorithm, new_password, salt)
        return

    def populate_result(self):
        try:
            self.result[self.response_attribute] = str(self.decoded_response['genPasswd'])
        except TypeError:
            if self.result['result'] == RESULT_SUCCESS:
                self.result[self.response_attribute] = True
            else:
                self.result[self.response_attribute] = False
                if self.connection.raise_exceptions:
                    from ...core.exceptions import LDAPOperationResult
                    raise LDAPOperationResult(result=self.result['result'], description=self.result['description'], dn=self.result['dn'], message=self.result['message'], response_type=self.result['type'])