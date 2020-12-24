# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\partition_entry_count.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from pyasn1.type.univ import Integer
from ...core.exceptions import LDAPExtensionError
from ..operation import ExtendedOperation
from ...protocol.rfc4511 import LDAPDN
from ...utils.asn1 import decoder
from ...utils.dn import safe_dn

class PartitionEntryCount(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.27.100.13'
        self.response_name = '2.16.840.1.113719.1.27.100.14'
        self.request_value = LDAPDN()
        self.response_attribute = 'entry_count'

    def __init__(self, connection, partition_dn, controls=None):
        ExtendedOperation.__init__(self, connection, controls)
        if connection.check_names:
            partition_dn = safe_dn(partition_dn)
        self.request_value = LDAPDN(partition_dn)

    def populate_result(self):
        substrate = self.decoded_response
        try:
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['entry_count'] = int(decoded)
        except Exception:
            raise LDAPExtensionError('unable to decode substrate')

        if substrate:
            raise LDAPExtensionError('unknown substrate remaining')