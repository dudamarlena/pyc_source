# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\nmasGetUniversalPassword.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from ...extend.operation import ExtendedOperation
from ...protocol.novell import NmasGetUniversalPasswordRequestValue, NmasGetUniversalPasswordResponseValue, NMAS_LDAP_EXT_VERSION
from ...utils.dn import safe_dn

class NmasGetUniversalPassword(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.39.42.100.13'
        self.response_name = '2.16.840.1.113719.1.39.42.100.14'
        self.request_value = NmasGetUniversalPasswordRequestValue()
        self.asn1_spec = NmasGetUniversalPasswordResponseValue()
        self.response_attribute = 'password'

    def __init__(self, connection, user, controls=None):
        ExtendedOperation.__init__(self, connection, controls)
        if connection.check_names:
            user = safe_dn(user)
        self.request_value['nmasver'] = NMAS_LDAP_EXT_VERSION
        self.request_value['reqdn'] = user

    def populate_result(self):
        if self.decoded_response:
            self.result['nmasver'] = int(self.decoded_response['nmasver'])
            self.result['error'] = int(self.decoded_response['err'])
            try:
                self.result['password'] = str(self.decoded_response['passwd']) if self.decoded_response['passwd'].hasValue() else None
            except TypeError:
                self.result['password'] = None

        return