# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\endTransaction.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from ...extend.operation import ExtendedOperation
from ...protocol.novell import EndGroupTypeRequestValue, EndGroupTypeResponseValue, Sequence
from ...utils.asn1 import decoder

class EndTransaction(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.27.103.2'
        self.response_name = '2.16.840.1.113719.1.27.103.2'
        self.request_value = EndGroupTypeRequestValue()
        self.asn1_spec = EndGroupTypeResponseValue()

    def __init__(self, connection, commit=True, controls=None):
        if controls and len(controls) == 1:
            group_cookie = decoder.decode(controls[0][2], asn1Spec=Sequence())[0][0]
        else:
            group_cookie = None
        controls = None
        ExtendedOperation.__init__(self, connection, controls)
        if group_cookie:
            self.request_value['endGroupCookie'] = group_cookie
            if not commit:
                self.request_value['endGroupValue'] = ''
        return

    def populate_result(self):
        try:
            self.result['value'] = self.decoded_response['endGroupValue']
        except TypeError:
            self.result['value'] = None

        return

    def set_response(self):
        self.response_value = self.result