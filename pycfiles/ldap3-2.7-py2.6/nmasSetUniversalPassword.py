# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\nmasSetUniversalPassword.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ...extend.operation import ExtendedOperation
from ...protocol.novell import NmasSetUniversalPasswordRequestValue, NmasSetUniversalPasswordResponseValue, NMAS_LDAP_EXT_VERSION
from ...utils.dn import safe_dn

class NmasSetUniversalPassword(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.39.42.100.11'
        self.response_name = '2.16.840.1.113719.1.39.42.100.12'
        self.request_value = NmasSetUniversalPasswordRequestValue()
        self.asn1_spec = NmasSetUniversalPasswordResponseValue()
        self.response_attribute = 'password'

    def __init__(self, connection, user, new_password, controls=None):
        ExtendedOperation.__init__(self, connection, controls)
        if connection.check_names and user:
            user = safe_dn(user)
        self.request_value['nmasver'] = NMAS_LDAP_EXT_VERSION
        if user:
            self.request_value['reqdn'] = user
        if new_password:
            self.request_value['new_passwd'] = new_password

    def populate_result(self):
        self.result['nmasver'] = int(self.decoded_response['nmasver'])
        self.result['error'] = int(self.decoded_response['err'])