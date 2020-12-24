# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\extend\microsoft\dirSync.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from ...core.exceptions import LDAPExtensionError
from ...protocol.microsoft import dir_sync_control, extended_dn_control, show_deleted_control
from ... import SUBTREE, DEREF_NEVER
from ...utils.dn import safe_dn

class DirSync(object):

    def __init__(self, connection, sync_base, sync_filter, attributes, cookie, object_security, ancestors_first, public_data_only, incremental_values, max_length, hex_guid):
        self.connection = connection
        if self.connection.check_names and sync_base:
            self.base = safe_dn(sync_base)
        else:
            self.base = sync_base
        self.filter = sync_filter
        self.attributes = attributes
        self.cookie = cookie
        self.object_security = object_security
        self.ancestors_first = ancestors_first
        self.public_data_only = public_data_only
        self.incremental_values = incremental_values
        self.max_length = max_length
        self.hex_guid = hex_guid
        self.more_results = True

    def loop(self):
        result = self.connection.search(search_base=self.base, search_filter=self.filter, search_scope=SUBTREE, attributes=self.attributes, dereference_aliases=DEREF_NEVER, controls=[
         dir_sync_control(criticality=True, object_security=self.object_security, ancestors_first=self.ancestors_first, public_data_only=self.public_data_only, incremental_values=self.incremental_values, max_length=self.max_length, cookie=self.cookie),
         extended_dn_control(criticality=False, hex_format=self.hex_guid),
         show_deleted_control(criticality=False)])
        if not self.connection.strategy.sync:
            (response, result) = self.connection.get_response(result)
        else:
            response = self.connection.response
            result = self.connection.result
        if result['description'] == 'success' and 'controls' in result and '1.2.840.113556.1.4.841' in result['controls']:
            self.more_results = result['controls']['1.2.840.113556.1.4.841']['value']['more_results']
            self.cookie = result['controls']['1.2.840.113556.1.4.841']['value']['cookie']
            return response
        if 'controls' in result:
            raise LDAPExtensionError('Missing DirSync control in response from server')
        else:
            raise LDAPExtensionError('error %r in DirSync' % result)