# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\replicaInfo.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from datetime import datetime
from pyasn1.type.univ import Integer
from ...core.exceptions import LDAPExtensionError
from ...protocol.novell import LDAPDN, ReplicaInfoRequestValue
from ..operation import ExtendedOperation
from ...utils.asn1 import decoder
from ...utils.dn import safe_dn

class ReplicaInfo(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.27.100.17'
        self.response_name = '2.16.840.1.113719.1.27.100.18'
        self.request_value = ReplicaInfoRequestValue()
        self.response_attribute = 'partition_dn'

    def __init__(self, connection, server_dn, partition_dn, controls=None):
        if connection.check_names:
            if server_dn:
                server_dn = safe_dn(server_dn)
            if partition_dn:
                partition_dn = safe_dn(partition_dn)
        ExtendedOperation.__init__(self, connection, controls)
        self.request_value['server_dn'] = server_dn
        self.request_value['partition_dn'] = partition_dn

    def populate_result(self):
        substrate = self.decoded_response
        try:
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['partition_id'] = int(decoded)
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['replica_state'] = int(decoded)
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['modification_time'] = datetime.utcfromtimestamp(int(decoded))
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['purge_time'] = datetime.utcfromtimestamp(int(decoded))
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['local_partition_id'] = int(decoded)
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=LDAPDN())
            self.result['partition_dn'] = str(decoded)
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['replica_type'] = int(decoded)
            (decoded, substrate) = decoder.decode(substrate, asn1Spec=Integer())
            self.result['flags'] = int(decoded)
        except Exception:
            raise LDAPExtensionError('unable to decode substrate')

        if substrate:
            raise LDAPExtensionError('unknown substrate remaining')