# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/routetable.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4033 bytes
"""
Represents a Route Table
"""
from boto.ec2.ec2object import TaggedEC2Object
from boto.resultset import ResultSet

class RouteTable(TaggedEC2Object):

    def __init__(self, connection=None):
        super(RouteTable, self).__init__(connection)
        self.id = None
        self.vpc_id = None
        self.routes = []
        self.associations = []

    def __repr__(self):
        return 'RouteTable:%s' % self.id

    def startElement(self, name, attrs, connection):
        result = super(RouteTable, self).startElement(name, attrs, connection)
        if result is not None:
            return result
        else:
            if name == 'routeSet':
                self.routes = ResultSet([('item', Route)])
                return self.routes
            if name == 'associationSet':
                self.associations = ResultSet([('item', RouteAssociation)])
                return self.associations
            return

    def endElement(self, name, value, connection):
        if name == 'routeTableId':
            self.id = value
        else:
            if name == 'vpcId':
                self.vpc_id = value
            else:
                setattr(self, name, value)


class Route(object):

    def __init__(self, connection=None):
        self.destination_cidr_block = None
        self.gateway_id = None
        self.instance_id = None
        self.interface_id = None
        self.vpc_peering_connection_id = None
        self.state = None
        self.origin = None

    def __repr__(self):
        return 'Route:%s' % self.destination_cidr_block

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'destinationCidrBlock':
            self.destination_cidr_block = value
        else:
            if name == 'gatewayId':
                self.gateway_id = value
            else:
                if name == 'instanceId':
                    self.instance_id = value
                else:
                    if name == 'networkInterfaceId':
                        self.interface_id = value
                    else:
                        if name == 'vpcPeeringConnectionId':
                            self.vpc_peering_connection_id = value
                        else:
                            if name == 'state':
                                self.state = value
                            elif name == 'origin':
                                self.origin = value


class RouteAssociation(object):

    def __init__(self, connection=None):
        self.id = None
        self.route_table_id = None
        self.subnet_id = None
        self.main = False

    def __repr__(self):
        return 'RouteAssociation:%s' % self.id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'routeTableAssociationId':
            self.id = value
        else:
            if name == 'routeTableId':
                self.route_table_id = value
            else:
                if name == 'subnetId':
                    self.subnet_id = value
                elif name == 'main':
                    self.main = value == 'true'