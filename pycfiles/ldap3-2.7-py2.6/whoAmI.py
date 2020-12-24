# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\standard\whoAmI.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ...extend.operation import ExtendedOperation
from ...utils.conv import to_unicode

class WhoAmI(ExtendedOperation):

    def config(self):
        self.request_name = '1.3.6.1.4.1.4203.1.11.3'
        self.response_attribute = 'authzid'

    def populate_result(self):
        try:
            self.result['authzid'] = to_unicode(self.decoded_response) if self.decoded_response else None
        except TypeError:
            self.result['authzid'] = self.decoded_response if self.decoded_response else None

        return