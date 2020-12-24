# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/ldap/pool.py
# Compiled at: 2013-05-17 11:12:20
import ldap
from ldappool import ConnectionManager
from threading import RLock
from ldapadapter.utility import ManageableLDAPAdapter, LDAPConnection
_pool = {}
_pool_lock = RLock()

class ManageableLDAPPoolAdapter(ManageableLDAPAdapter):
    """LDAP adapter using connection pool"""

    def connect(self, dn=None, password=None):
        conn_str = self.getServerURL()
        connection = _pool.get(conn_str)
        if connection is None:
            with _pool_lock:
                connection = _pool[conn_str] = ConnectionManager(conn_str)
        if dn is None:
            dn = self.bindDN or ''
            password = self.bindPassword or ''
        with connection.connection(dn, password) as (conn):
            try:
                conn.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
            except ldap.LDAPError:
                raise Exception('Server should be LDAP v3')

            return LDAPConnection(conn)
        return