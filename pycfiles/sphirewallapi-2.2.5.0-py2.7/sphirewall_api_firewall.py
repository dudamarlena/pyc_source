# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sphirewallapi/sphirewall_api_firewall.py
# Compiled at: 2018-06-20 19:57:46


class FirewallSettings:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def fingerprints_list(self):
        return self.connection.request('firewall/fingerprints/list', {})['fingerprints']

    def watchdog_last(self):
        return self.connection.request('firewall/watchdog/last', {})['last']

    def watchdog_count(self):
        return self.connection.request('firewall/watchdog/count', {})['count']

    def connections_list(self, mac=None, ip=None, user=None, time=None):
        args = {}
        if mac:
            args['mac'] = mac
        if ip:
            args['ip'] = ip
        if user:
            args['user'] = user
        if time:
            args['filterTime'] = time
        return self.connection.request('firewall/tracker/list', args)['connections']

    def connections_list_group(self, group):
        args = {'group': group}
        return self.connection.request('firewall/tracker/list/group', args)['connections']

    def webfilter_search(self, term):
        args = {'term': term}
        return self.connection.request('firewall/webfilter/rules/search', args)['policies']

    def connections_list_applications(self, filter_group=None, filter_user=None):
        args = {}
        if filter_group:
            args['filter_group'] = filter_group
        if filter_user:
            args['filter_user'] = filter_user
        return self.connection.request('firewall/tracker/applications', args)['applications']

    def connections_list_applications_users(self, application, filter_group=None):
        args = {'application': application}
        if filter_group:
            args['filter_group'] = filter_group
        return self.connection.request('firewall/tracker/applications/users', args)['users']

    def connections_list_protocols(self):
        args = {}
        return self.connection.request('firewall/tracker/protocols', args)['protocols']

    def connections_list_hosts(self):
        args = {}
        return self.connection.request('firewall/tracker/hosts', args)['hosts']

    def connections_stats(self):
        return self.connection.request('firewall/tracker/details', None)

    def connection_details(self, connection_id):
        return self.connection.request('firewall/tracker/connection/details', {'id': connection_id})

    def connections_size(self):
        return self.connection.request('firewall/tracker/size', None)['size']

    def signatures(self):
        return self.connection.request('firewall/signatures', {})['signatures']

    def signatures_import(self, url=None):
        params = {}
        if url:
            params = {'url': url}
        return self.connection.request('firewall/signatures/import', params)['imported']

    def signatures_search(self, term):
        return self.connection.request('firewall/signatures/search', {'term': term})['signatures']

    def connection_terminate(self, connection_id):
        self.connection.request('firewall/tracker/terminate', {'id': connection_id})

    def geoip_countries(self):
        return self.connection.request('firewall/geoip/list', {})['countries']