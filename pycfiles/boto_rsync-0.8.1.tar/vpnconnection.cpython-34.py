# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/vpnconnection.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7722 bytes
import boto
from datetime import datetime
from boto.resultset import ResultSet
from boto.ec2.ec2object import TaggedEC2Object

class VpnConnectionOptions(object):
    """VpnConnectionOptions"""

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
    """VpnStaticRoute"""

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
    """VpnTunnel"""

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
    """VpnConnection"""

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