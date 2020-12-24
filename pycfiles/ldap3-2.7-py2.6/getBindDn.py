# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\getBindDn.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ...protocol.novell import Identity
from ...extend.operation import ExtendedOperation

class GetBindDn(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.27.100.31'
        self.response_name = '2.16.840.1.113719.1.27.100.32'
        self.response_attribute = 'identity'
        self.asn1_spec = Identity()

    def populate_result(self):
        try:
            self.result['identity'] = str(self.decoded_response) if self.decoded_response else None
        except TypeError:
            self.result['identity'] = None

        return