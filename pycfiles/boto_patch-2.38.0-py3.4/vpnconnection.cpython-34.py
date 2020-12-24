# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/vpnconnection.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7722 bytes
import boto
from datetime import datetime
from boto.resultset import ResultSet
from boto.ec2.ec2object import TaggedEC2Object

class VpnConnectionOptions(object):
    __doc__ = "\n    Represents VPN connection options\n\n    :ivar static_routes_only: Indicates whether the VPN connection uses static\n        routes only.  Static routes must be used for devices that don't support\n        BGP.\n\n    "

    def __init__(self, static_routes_only=None):
        self.static_routes_only = static_routes_only

    def __repr__(self):
        return 'VpnConnectionOptions'

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'staticRoutesOnly':
            self.static_routes_only = True if value == 'true' else False
        else:
            setattr(self, name, value)


class VpnStaticRoute(object):
    __doc__ = '\n    Represents a static route for a VPN connection.\n\n    :ivar destination_cidr_block: The CIDR block associated with the local\n        subnet of the customer data center.\n    :ivar source: Indicates how the routes were provided.\n    :ivar state: The current state of the static route.\n    '

    def __init__(self, destination_cidr_block=None, source=None, state=None):
        self.destination_cidr_block = destination_cidr_block
        self.source = source
        self.available = state

    def __repr__(self):
        return 'VpnStaticRoute: %s' % self.destination_cidr_block

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'destinationCidrBlock':
            self.destination_cidr_block = value
        else:
            if name == 'source':
                self.source = value
            else:
                if name == 'state':
                    self.state = value
                else:
                    setattr(self, name, value)


class VpnTunnel(object):
    __doc__ = "\n    Represents telemetry for a VPN tunnel\n\n    :ivar outside_ip_address: The Internet-routable IP address of the\n        virtual private gateway's outside interface.\n    :ivar status: The status of the VPN tunnel. Valid values: UP | DOWN\n    :ivar last_status_change: The date and time of the last change in status.\n    :ivar status_message: If an error occurs, a description of the error.\n    :ivar accepted_route_count: The number of accepted routes.\n    "

    def __init__(self, outside_ip_address=None, status=None, last_status_change=None, status_message=None, accepted_route_count=None):
        self.outside_ip_address = outside_ip_address
        self.status = status
        self.last_status_change = last_status_change
        self.status_message = status_message
        self.accepted_route_count = accepted_route_count

    def __repr__(self):
        return 'VpnTunnel: %s' % self.outside_ip_address

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'outsideIpAddress':
            self.outside_ip_address = value
        else:
            if name == 'status':
                self.status = value
            else:
                if name == 'lastStatusChange':
                    self.last_status_change = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    if name == 'statusMessage':
                        self.status_message = value
                    else:
                        if name == 'acceptedRouteCount':
                            try:
                                value = int(value)
                            except ValueError:
                                boto.log.warning('Error converting code (%s) to int' % value)

                            self.accepted_route_count = value
                        else:
                            setattr(self, name, value)


class VpnConnection(TaggedEC2Object):
    __doc__ = "\n    Represents a VPN Connection\n\n    :ivar id: The ID of the VPN connection.\n    :ivar state: The current state of the VPN connection.\n        Valid values: pending | available | deleting | deleted\n    :ivar customer_gateway_configuration: The configuration information for the\n        VPN connection's customer gateway (in the native XML format). This\n        element is always present in the\n        :class:`boto.vpc.VPCConnection.create_vpn_connection` response;\n        however, it's present in the\n        :class:`boto.vpc.VPCConnection.get_all_vpn_connections` response only\n        if the VPN connection is in the pending or available state.\n    :ivar type: The type of VPN connection (ipsec.1).\n    :ivar customer_gateway_id: The ID of the customer gateway at your end of\n        the VPN connection.\n    :ivar vpn_gateway_id: The ID of the virtual private gateway\n        at the AWS side of the VPN connection.\n    :ivar tunnels: A list of the vpn tunnels (always 2)\n    :ivar options: The option set describing the VPN connection.\n    :ivar static_routes: A list of static routes associated with a VPN\n        connection.\n\n    "

    def __init__(self, connection=None):
        super(VpnConnection, self).__init__(connection)
        self.id = None
        self.state = None
        self.customer_gateway_configuration = None
        self.type = None
        self.customer_gateway_id = None
        self.vpn_gateway_id = None
        self.tunnels = []
        self.options = None
        self.static_routes = []

    def __repr__(self):
        return 'VpnConnection:%s' % self.id

    def startElement(self, name, attrs, connection):
        retval = super(VpnConnection, self).startElement(name, attrs, connection)
        if retval is not None:
            return retval
        if name == 'vgwTelemetry':
            self.tunnels = ResultSet([('item', VpnTunnel)])
            return self.tunnels
        if name == 'routes':
            self.static_routes = ResultSet([('item', VpnStaticRoute)])
            return self.static_routes
        if name == 'options':
            self.options = VpnConnectionOptions()
            return self.options

    def endElement(self, name, value, connection):
        if name == 'vpnConnectionId':
            self.id = value
        else:
            if name == 'state':
                self.state = value
            else:
                if name == 'customerGatewayConfiguration':
                    self.customer_gateway_configuration = value
                else:
                    if name == 'type':
                        self.type = value
                    else:
                        if name == 'customerGatewayId':
                            self.customer_gateway_id = value
                        else:
                            if name == 'vpnGatewayId':
                                self.vpn_gateway_id = value
                            else:
                                setattr(self, name, value)

    def delete(self, dry_run=False):
        return self.connection.delete_vpn_connection(self.id, dry_run=dry_run)