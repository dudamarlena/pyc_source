# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\novell\listReplicas.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ...extend.operation import ExtendedOperation
from ...protocol.novell import ReplicaList
from ...protocol.rfc4511 import LDAPDN
from ...utils.dn import safe_dn

class ListReplicas(ExtendedOperation):

    def config(self):
        self.request_name = '2.16.840.1.113719.1.27.100.19'
        self.response_name = '2.16.840.1.113719.1.27.100.20'
        self.request_value = LDAPDN()
        self.asn1_spec = ReplicaList()
        self.response_attribute = 'replicas'

    def __init__(self, connection, server_dn, controls=None):
        ExtendedOperation.__init__(self, connection, controls)
        if connection.check_names:
            server_dn = safe_dn(server_dn)
        self.request_value = LDAPDN(server_dn)

    def populate_result(self):
        try:
            self.result['replicas'] = [ str(replica) for replica in self.decoded_response ] if self.decoded_response else None
        except TypeError:
            self.result['replicas'] = None

        return