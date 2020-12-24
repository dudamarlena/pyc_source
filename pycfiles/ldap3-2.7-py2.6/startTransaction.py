# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\startTransaction.py
# Compiled at: 2020-02-23 02:04:03
"""
"""
from ...extend.operation import ExtendedOperation
from ...protocol.novell import CreateGroupTypeRequestValue, CreateGroupTypeResponseValue, GroupingControlValue
from ...protocol.controls import build_control

class StartTransaction(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.27.103.1'
        self.response_name = '2.16.840.1.113719.1.27.103.1'
        self.request_value = CreateGroupTypeRequestValue()
        self.asn1_spec = CreateGroupTypeResponseValue()

    def __init__(self, connection, controls=None):
        ExtendedOperation.__init__(self, connection, controls)
        self.request_value['createGroupType'] = '2.16.840.1.113719.1.27.103.7'

    def populate_result(self):
        self.result['cookie'] = int(self.decoded_response['createGroupCookie'])
        try:
            self.result['value'] = self.decoded_response['createGroupValue']
        except TypeError:
            self.result['value'] = None

        return

    def set_response(self):
        try:
            grouping_cookie_value = GroupingControlValue()
            grouping_cookie_value['groupingCookie'] = self.result['cookie']
            self.response_value = build_control('2.16.840.1.113719.1.27.103.7', True, grouping_cookie_value, encode_control_value=True)
        except TypeError:
            self.response_value = None

        return