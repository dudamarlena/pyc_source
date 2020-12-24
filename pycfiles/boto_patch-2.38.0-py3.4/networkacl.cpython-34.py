# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/networkacl.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4976 bytes
"""
Represents a Network ACL
"""
from boto.ec2.ec2object import TaggedEC2Object
from boto.resultset import ResultSet

class Icmp(object):
    __doc__ = '\n    Defines the ICMP code and type.\n    '

    def __init__(self, connection=None):
        self.code = None
        self.type = None

    def __repr__(self):
        return 'Icmp::code:%s, type:%s)' % (self.code, self.type)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'code':
            self.code = value
        elif name == 'type':
            self.type = value


class NetworkAcl(TaggedEC2Object):

    def __init__(self, connection=None):
        super(NetworkAcl, self).__init__(connection)
        self.id = None
        self.vpc_id = None
        self.network_acl_entries = []
        self.associations = []

    def __repr__(self):
        return 'NetworkAcl:%s' % self.id

    def startElement(self, name, attrs, connection):
        result = super(NetworkAcl, self).startElement(name, attrs, connection)
        if result is not None:
            return result
        else:
            if name == 'entrySet':
                self.network_acl_entries = ResultSet([('item', NetworkAclEntry)])
                return self.network_acl_entries
            if name == 'associationSet':
                self.associations = ResultSet([('item', NetworkAclAssociation)])
                return self.associations
            return

    def endElement(self, name, value, connection):
        if name == 'networkAclId':
            self.id = value
        else:
            if name == 'vpcId':
                self.vpc_id = value
            else:
                setattr(self, name, value)


class NetworkAclEntry(object):

    def __init__(self, connection=None):
        self.rule_number = None
        self.protocol = None
        self.rule_action = None
        self.egress = None
        self.cidr_block = None
        self.port_range = PortRange()
        self.icmp = Icmp()

    def __repr__(self):
        return 'Acl:%s' % self.rule_number

    def startElement(self, name, attrs, connection):
        if name == 'portRange':
            return self.port_range
        else:
            if name == 'icmpTypeCode':
                return self.icmp
            return

    def endElement(self, name, value, connection):
        if name == 'cidrBlock':
            self.cidr_block = value
        else:
            if name == 'egress':
                self.egress = value
            else:
                if name == 'protocol':
                    self.protocol = value
                else:
                    if name == 'ruleAction':
                        self.rule_action = value
                    elif name == 'ruleNumber':
                        self.rule_number = value


class NetworkAclAssociation(object):

    def __init__(self, connection=None):
        self.id = None
        self.subnet_id = None
        self.network_acl_id = None

    def __repr__(self):
        return 'NetworkAclAssociation:%s' % self.id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'networkAclAssociationId':
            self.id = value
        else:
            if name == 'networkAclId':
                self.network_acl_id = value
            elif name == 'subnetId':
                self.subnet_id = value


class PortRange(object):
    __doc__ = '\n    Define the port range for the ACL entry if it is tcp / udp\n    '

    def __init__(self, connection=None):
        self.from_port = None
        self.to_port = None

    def __repr__(self):
        return 'PortRange:(%s-%s)' % (self.from_port, self.to_port)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'from':
            self.from_port = value
        elif name == 'to':
            self.to_port = value