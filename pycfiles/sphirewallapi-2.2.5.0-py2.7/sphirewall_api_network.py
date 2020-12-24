# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sphirewallapi/sphirewall_api_network.py
# Compiled at: 2018-06-20 19:57:46


class NetworkSettings:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def devices(self, device=None, configured=False):
        if device is not None:
            allDevices = self.devices(configured=configured)
            for d in allDevices:
                if d['interface'] == device:
                    return d

        return self.connection.request('network/devices/list', {'configuredDevices': configured})['devices']

    def devices_remove(self, device):
        self.connection.request('network/devices/delete', {'device': device})

    def devices_up(self, device):
        self.connection.request('network/devices/up', {'device': device})

    def devices_dhcp_renew(self, device):
        self.connection.request('network/devices/dhcp/refresh', {'interface': device})

    def devices_down(self, device):
        self.connection.request('network/devices/down', {'device': device})

    def devices_refresh(self, device):
        self.connection.request('network/devices/refresh', {'device': device})

    def devices_save(self):
        self.connection.request('network/devices/save', {})

    def devices_set(self, device=None, device_params=None, address_params=None, dhcp_server=None, pppoe=None, upstream_proxy=None):
        args = {}
        if device:
            args['interface'] = device
        if device_params.get('vlan', False):
            args['vlan'] = True
            args['vlanId'] = device_params['vlanId']
            args['vlanInterface'] = device_params['vlanInterface']
        if device_params.get('bridge', False):
            args['bridge'] = True
            args['bridgeDevices'] = device_params['bridgeDevices']
            args['bridge_hub_mode'] = device_params.get('bridge_hub_mode')
        if device_params.get('lacp', False):
            args['lacp'] = True
            args['lacpDevices'] = device_params['lacpDevices']
            args['lacpMode'] = device_params['lacpMode']
            args['lacpLinkStatePollFrequency'] = device_params['lacpLinkStatePollFrequency']
            args['lacpLinkStateDownDelay'] = device_params['lacpLinkStateDownDelay']
            args['lacpLinkStateUpDelay'] = device_params['lacpLinkStateUpDelay']
        if device_params.get('physical', False):
            args['physical'] = True
            args['physicalInterface'] = device_params.get('physicalInterface')
        if device_params.get('autoneg', True):
            args['autoneg'] = True
        else:
            args['autoneg'] = False
            args['speed'] = device_params.get('speed')
            args['full_duplex'] = device_params.get('full_duplex')
        if 'wan' in device_params:
            args['wan'] = device_params.get('wan')
        if 'wan_uplink_primary' in device_params:
            args['wan_uplink_primary'] = device_params.get('wan_uplink_primary')
        if address_params:
            if 'ipv4' in address_params:
                args['ipv4'] = address_params.get('ipv4')
            if 'dhcp' in address_params:
                args['dhcp'] = address_params.get('dhcp')
            if 'gateway' in address_params:
                args['gateway'] = address_params.get('gateway')
            if 'configured_mac_address' in address_params:
                args['configured_mac_address'] = address_params.get('configured_mac_address')
        if pppoe:
            args['pppoe_enabled'] = pppoe.get('pppoe_enabled', False)
            args['pppoe_username'] = pppoe.get('pppoe_username', '')
            args['pppoe_password'] = pppoe.get('pppoe_password', '')
        if upstream_proxy:
            args['upstream_enabled'] = upstream_proxy.get('upstream_enabled', False)
            args['upstream_proxy_uri'] = upstream_proxy.get('upstream_proxy_uri', '')
            args['upstream_enabled_ports'] = upstream_proxy.get('upstream_enabled_ports', [])
            args['upstream_enabled_exceptions'] = upstream_proxy.get('upstream_enabled_exceptions', [])
        if dhcp_server:
            args['dhcpServerMode'] = dhcp_server.get('dhcpServerMode')
            args['dhcpServerStart'] = dhcp_server.get('dhcpServerStart')
            args['dhcpServerEnd'] = dhcp_server.get('dhcpServerEnd')
            args['dhcpServerRelay'] = dhcp_server.get('dhcpServerRelay')
            args['dhcpServerLeaseTime'] = dhcp_server.get('dhcpServerLeaseTime')
            args['dhcpServerDnsMode'] = dhcp_server.get('dhcpServerDnsMode')
            args['dhcpServerDnsServer'] = dhcp_server.get('dhcpServerDnsServer')
            args['dhcpServerTftpEnabled'] = dhcp_server.get('dhcpServerTftpEnabled')
            args['dhcpServerTftpServer'] = dhcp_server.get('dhcpServerTftpServer')
            args['dhcpServerTftpFilename'] = dhcp_server.get('dhcpServerTftpFilename')
        if 'name' in device_params:
            args['name'] = device_params.get('name', '')
        if 'persisted' in device_params:
            args['persisted'] = device_params.get('persisted', False)
        self.connection.request('network/devices/set', args)

    def devices_aliases_add(self, device, ip):
        args = {'interface': device, 'ip': ip}
        self.connection.request('network/devices/alias/add', args)

    def devices_aliases_del(self, device, ip):
        args = {'interface': device, 'ip': ip}
        self.connection.request('network/devices/alias/delete', args)

    def devices_ddns(self, device, ddenabled, ddusername, ddpassword, dddomain):
        args = {'interface': device, 'ddenabled': ddenabled, 'ddusername': ddusername, 'ddpassword': ddpassword, 'dddomain': dddomain}
        self.connection.request('network/devices/dynamicdns/set', args)

    def devices_dhcp_static_add(self, device, ip, mac):
        args = {'device': device, 'ip': ip, 'mac': mac}
        self.connection.request('network/devices/leases/add', args)

    def devices_dhcp_static_del(self, device, ip, mac):
        args = {'device': device, 'ip': ip, 'mac': mac}
        self.connection.request('network/devices/leases/del', args)

    def devices_toggle(self, device):
        args = {'interface': device}
        self.connection.request('network/devices/toggle', args)

    def routes(self):
        return self.connection.request('network/routes/list', None)['routes']

    def routes_active(self):
        return self.connection.request('network/routes/list', None)['active_routes']

    def routes_add(self, destination=None, destination_cidr=None, route_device=None, route_nexthop=None):
        args = {}
        if destination and destination_cidr:
            args['destination'] = destination
            args['destination_cidr'] = int(destination_cidr)
        if route_device:
            args['route_device'] = route_device
        if route_nexthop:
            args['route_nexthop'] = route_nexthop
        self.connection.request('network/routes/add', args)

    def routes_del(self, id):
        args = {'id': id}
        self.connection.request('network/routes/del', args)

    def connections(self, name=None):
        if name is not None:
            allConnections = self.connections()
            for conn in allConnections:
                if conn['name'] == name:
                    return conn

        return self.connection.request('network/connections/list', {})['items']

    def dns_config(self):
        return self.connection.request('network/dns/get', None)

    def dns_config_set(self, nameserver):
        self.connection.request('network/dns/set', {'nameserver': nameserver})

    def vpns(self, name=None):
        if name is not None:
            for vpn in self.vpns():
                if vpn['name'] == name:
                    return vpn

            return
        return self.connection.request('network/vpn', None)['items']

    def vpns_clientvpn(self):
        return self.connection.request('network/clientvpn', None)

    def devices_createbridge(self):
        return self.connection.request('network/devices/createbridge', None)

    def ping(self, hostname):
        connection_request = self.connection.request('network/ping', {'host': hostname})
        return connection_request['result']

    def dig(self, hostname):
        connection_request = self.connection.request('network/dig', {'hostname': hostname})
        return connection_request['result']

    def traceroute(self, hostname):
        connection_request = self.connection.request('network/traceroute', {'hostname': hostname})
        return connection_request['result']

    def capture(self):
        return self.connection.request('network/capture', {})

    def capture_raw(self):
        return self.connection.request('network/capture/raw', {})

    def capture_start(self, interface, type=None, target=''):
        return self.connection.request('network/capture/start', {'interface': interface, 'type': type, 'target': target})

    def capture_stop(self):
        return self.connection.request('network/capture/stop', {})