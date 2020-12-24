# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sphirewallapi/sphirewall_api_general.py
# Compiled at: 2018-06-20 19:57:46


class GeneralSettings:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def hosts_list(self):
        return self.connection.request('network/arp/list', None)['hosts']

    def hosts_size(self):
        return self.connection.request('network/arp/size', None)['size']

    def host(self, ip):
        all_active_hosts = self.hosts_list()
        for host in all_active_hosts:
            if host['host'] == ip:
                return host

        return

    def active_users_list(self):
        return self.connection.request('auth/sessions/list', None)['sessions']

    def active_users_by_group(self, group_name):
        return self.connection.request('auth/sessions/group/list', {'groupname': group_name})['sessions']

    def list_persisted_session(self):
        return self.connection.request('auth/sessions/list', None)['persisted']

    def create_persisted_session(self, username, mac):
        return self.connection.request('auth/sessions/persist', {'username': username, 'hw': mac})

    def check_persisted_session(self, mac):
        return self.connection.request('auth/sessions/persist/check', {'hw': mac})['persisted']

    def delete_persisted_session(self, username, mac):
        self.connection.request('auth/sessions/persist/remove', {'username': username, 'hw': mac})

    def delete_persisted_session_by_group(self, group):
        self.connection.request('auth/sessions/persist/remove/group', {'group': group})

    def delete_persisted_session_list(self, sessions):
        self.connection.request('auth/sessions/persist/remove/list', {'sessions': sessions})

    def list_persisted_session_exceptions(self):
        return self.connection.request('auth/sessions/persist/exceptions/list', None)['exceptions']

    def add_persisted_session_exception(self, mac):
        return self.connection.request('auth/sessions/persist/exceptions/add', {'hw': mac})

    def remove_persisted_session_exception(self, mac):
        return self.connection.request('auth/sessions/persist/exceptions/remove', {'hw': mac})

    def configuration(self, key, value=None):
        if value is not None:
            arr = {'key': key, 'value': value}
            self.connection.request('general/config/set', arr)
        else:
            arr = {'key': key, 'hideExceptions': True}
            retval = self.connection.request('general/config/get', arr)
            if retval is not None:
                return retval['value']
            return False
        return

    def configuration_dump(self):
        return self.connection.request('general/config', {})['dump']

    def configuration_loaded(self):
        return self.connection.request('general/config/loaded', {})['loaded']

    def configuration_create_local_snapshot(self):
        return self.connection.request('general/config/snapshot/local', {})

    def configuration_load(self, snapshot):
        return self.connection.request('general/config/load', {'snapshot': snapshot})

    def groups(self, groupid=None, groupname=None, archived=False):
        if groupid is not None:
            return self.connection.request('auth/groups/get', {'id': int(groupid)})
        else:
            if groupname is not None:
                return self.connection.request('auth/groups/get', {'name': groupname})
            if archived:
                return self.connection.request('auth/groups/list/all', None)['groups']
            return self.connection.request('auth/groups/list', None)['groups']

    def groups_with_members(self, archived=False):
        return self.connection.request('auth/groups/list/w/members', {'archived': archived})['groups']

    def groups_list_by_owner(self, username):
        return self.connection.request('auth/groups/list/by/owner', {'owner': username})['groups']

    def users_check_for_group(self, username, group=None, groups=None):
        args = {'username': username}
        if group:
            args['group'] = group
        if groups:
            args['groups'] = groups
        return self.connection.request('auth/users/groups/check', args)['is_member']

    def groups_get_by_name(self, name):
        return self.groups(groupname=name)

    def users(self, username=None, archived=False, filter_group=None):
        if username is not None:
            return self.connection.request('auth/users/get', {'username': username})
        else:
            if archived or filter_group:
                args = {}
                if archived:
                    args['archived'] = archived
                if filter_group:
                    args['filter_group'] = filter_group
                return self.connection.request('auth/users/list/filtered', args)['users']
            return self.connection.request('auth/users/list', {})['users']

    def users_add(self, username):
        args = {'username': username}
        self.connection.request('auth/users/add', args)

    def users_add_bulk(self, users):
        self.connection.request('auth/users/add/bulk', {'users': users})

    def users_delete(self, username):
        args = {'username': username}
        self.connection.request('auth/users/del', args)

    def users_save(self, username, fname, lname, email, archived=False, temp_user=False, expiry_timestamp=-1, expiry_after_login=-1, provider=None, dn=None, description=None, is_guest=False):
        args = {'username': username, 
           'fname': fname, 
           'lname': lname, 
           'email': email, 
           'temp_user': temp_user, 
           'expiry_timestamp': expiry_timestamp, 
           'expiry_after_login': expiry_after_login, 
           'archived': archived, 
           'description': description, 
           'is_guest': is_guest}
        if provider:
            args['provider'] = provider
        if dn:
            args['dn'] = dn
        self.connection.request('auth/users/save', args)

    def user_set_password(self, username, password):
        args = {'username': username, 'password': password}
        self.connection.request('auth/users/setpassword', args)

    def group_add(self, name, provider=None, owners=None, domain=None, dn=None):
        args = {'name': name}
        if provider:
            args['provider'] = provider
        if owners:
            args['owners'] = owners
        if domain:
            args['domain'] = domain
        if dn:
            args['dn'] = domain
        self.connection.request('auth/groups/create', args)

    def group_archive(self, groups, provider):
        args = {'groups': groups, 'provider': provider}
        return self.connection.request('auth/groups/archive', args).get('group_count')

    def users_archive(self, users, provider):
        args = {'users': users, 'provider': provider}
        return self.connection.request('auth/users/archive', args).get('user_count')

    def group_set_owners(self, group, owners):
        args = {'name': group, 'owners': owners}
        self.connection.request('auth/groups/setowners', args)

    def group_addsubgroups(self, name, sub_groups):
        args = {'name': name, 'sub_groups': sub_groups}
        self.connection.request('auth/groups/addsubgroups', args)

    def groups_delete(self, id=None, name=None):
        args = {}
        if id is not None:
            args['id'] = int(id)
        if name is not None:
            args['name'] = name
        self.connection.request('auth/groups/del', args)
        return

    def groups_create_bulk(self, groups):
        self.connection.request('auth/groups/create/bulk', {'values': groups})

    def user_createormodify(self, username, firstname, lastname, password, groups):
        user_details = {'username': username, 
           'fname': firstname, 
           'lname': lastname, 
           'password': password, 
           'groups': groups}
        self.connection.request('auth/user/merge', user_details)

    def groups_save(self, groupId, manager, isAdmin, description, archived=False, metadata='', sub_groups=[], owners=[]):
        args = {'id': int(groupId), 
           'desc': description, 
           'manager': manager, 
           'mui': isAdmin, 
           'metadata': metadata, 
           'sub_groups': sub_groups, 
           'owners': owners, 
           'archived': archived}
        self.connection.request('auth/groups/save', args)

    def disconnect_session(self, address=None, mac_address=None):
        args = {}
        if address:
            args['ipaddress'] = address
        if mac_address:
            args['mac_address'] = mac_address
        self.connection.request('auth/logout', args)

    def events_types(self):
        return self.connection.request('general/event/types', None)['event_types']

    def users_groups_merge(self, username, groups, group_provider=None):
        args = {'username': username, 'groups': groups}
        if group_provider:
            args['provider'] = group_provider
        self.connection.request('auth/groups/mergeoveruser', args)

    def user_groups_add(self, username, groupid):
        args = {'username': username, 'group': int(groupid)}
        self.connection.request('auth/users/groups/add', args)

    def user_groups_remove(self, username, groupid):
        args = {'username': username, 'group': int(groupid)}
        self.connection.request('auth/users/groups/del', args)

    def user_enable(self, username):
        args = {'username': username}
        self.connection.request('auth/users/enable', args)

    def user_disable(self, username):
        args = {'username': username}
        self.connection.request('auth/users/disable', args)

    def advanced(self, key=None, value=None):
        if key is None and value is None:
            args = {}
            return self.connection.request('general/runtime/list', args)['keys']
        else:
            args = {'key': key, 'value': value}
            self.connection.request('general/runtime/set', args)
            return

    def advanced_value(self, key):
        all_items = self.advanced()
        for item in all_items:
            if item['key'] == key:
                return item['value']

        return

    def logs(self, filter=None, no_lines=100):
        args = {'no_lines': no_lines}
        if filter is not None:
            args['filter'] = filter
        return self.connection.request('general/os/logs', args)['log']

    def ldap(self, scope_id=None):
        if not scope_id:
            return self.connection.request('auth/ldap', None)
        else:
            return self.connection.request('auth/ldap', {'scope_id': scope_id})

    def radius(self):
        return self.connection.request('auth/radius', None)

    def logging(self, context=None, priority=None):
        if context is not None and priority is not None:
            self.connection.request('general/logging/set', {'context': context, 'level': priority})
        return self.connection.request('general/logging/list', {})['levels']

    def logging_critical(self, value=None):
        if value is not None:
            self.connection.request('general/logging/critical', {'critical': value})
        return self.connection.request('general/logging/critical', {})['critical']

    def logging_delete(self, context):
        self.connection.request('general/logging/remove', {'context': context})

    def configuration_bulk(self, values):
        self.connection.request('general/config/set/bulk', {'values': values})

    def authentication_syslog(self):
        return self.connection.request('auth/syslog', {})

    def create_session(self, ip, mac_address, username, timeout=-1, absolute_timeout=False, create_user_if_missing=False, authentication_provider=None, user_provider=None):
        req = {'ipaddress': ip, 
           'mac': mac_address, 
           'username': username, 
           'create_user': create_user_if_missing, 
           'timeout': timeout, 
           'absoluteTimeout': absolute_timeout}
        if authentication_provider:
            req['authentication_provider'] = authentication_provider
        if user_provider:
            req['provider'] = user_provider
        self.connection.request('auth/createsession', req)

    def session_network_based_timeouts(self):
        return self.connection.request('auth/sessions/networktimeouts', None)['timeouts']

    def session_network_based_timeouts_create_or_modify(self, id=None, timeout=0, type=0, mon=False, tues=False, wed=False, thur=False, fri=False, sat=False, sun=False, networks=[], groups=[], user_device_limit=0):
        args = {'timeout': timeout, 
           'networks': networks, 
           'groups': groups, 
           'type': type, 
           'user_device_limit': user_device_limit, 
           'mon': mon, 
           'tues': tues, 
           'wed': wed, 
           'thur': thur, 
           'fri': fri, 
           'sat': sat, 
           'sun': sun}
        if id:
            args['id'] = id
        return self.connection.request('auth/sessions/networktimeouts/manage', args)

    def session_network_based_timeouts_remove(self, id=None):
        return self.connection.request('auth/sessions/networktimeouts/remove', {'id': id})

    def cloud_connected(self):
        return self.connection.request('general/cloud/connected', None)['status']

    def metrics(self):
        return self.connection.request('general/metrics', None)['points']

    def metrics_spec(self, metric):
        return self.connection.request('general/metrics/spec', {'metric': metric})['points']

    def install_watchdog(self, identifier):
        return self.connection.request('general/installwatchdog', {'id': identifier})

    def wmi(self):
        return self.connection.request('auth/wmic', None)

    def sphireos_version(self):
        return self.connection.request('general/os/version', None)

    def sphireos_update_start(self):
        return self.connection.request('general/os/update/start', None)

    def sphireos_update_status(self):
        return self.connection.request('general/os/update/status', None)

    def sphireos_restart(self):
        return self.connection.request('general/os/restart', None)

    def cloud_set(self, deviceid, key, region, enabled, verify=True, proxy_url=''):
        args = {'deviceid': deviceid, 
           'key': key, 
           'region': region, 
           'enabled': enabled, 
           'verify': verify, 
           'proxy_url': proxy_url}
        self.connection.request('general/cloud/set', args)

    def cloud_get(self):
        return self.connection.request('general/cloud', None)

    def cloud_configuration_sync(self):
        return self.connection.request('general/cloud/config/sync', None)

    def realm_login(self, username, password, realm):
        args = {'username': username, 
           'password': password, 
           'realm': realm}
        return self.connection.request('auth/realm/login', args)