# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/ooldap/foundation.py
# Compiled at: 2015-10-07 16:05:24
import os, ldap
from ooldap import Connection

class LDAPObject(object):

    def __init__(self, dn, uri=os.environ['LDAP_CONNECTION_URI'], bind_dn=os.environ['LDAP_CONNECTION_DN'], password=os.environ['LDAP_CONNECTION_PASSWORD']):
        self.dn = dn
        assert dn
        self.connection = Connection(uri, bind_dn, password)

    @property
    def data(self):
        self.connection.bind()
        result_id = self.connection.stream.search(self.dn, ldap.SCOPE_BASE, '(&)', None)
        type, data = self.connection.stream.result(result_id, 10)
        self.connection.unbind()
        if len(data) == 0:
            raise ldap.NO_RESULTS_RETURNED
            return
        else:
            if len(data) > 1:
                raise ldap.RESULTS_TOO_LARGE
            return data[0][1]

    def get_attribute(self, attribute):
        if not self.data:
            return None
        else:
            if attribute not in self.data:
                return None
            attribute = self.data[attribute]
            if len(attribute) == 1:
                return attribute[0]
            return attribute

    @property
    def cn(self):
        return self.get_attribute('cn')

    @property
    def memberOf(self):
        return self.get_attribute('memberOf')

    @property
    def description(self):
        return self.get_attribute('description')