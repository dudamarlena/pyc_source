# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/subnet.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2101 bytes
__doc__ = '\nRepresents a Subnet\n'
from boto.ec2.ec2object import TaggedEC2Object

class Subnet(TaggedEC2Object):

    def __init__(self, connection=None):
        super(Subnet, self).__init__(connection)
        self.id = None
        self.vpc_id = None
        self.state = None
        self.cidr_block = None
        self.available_ip_address_count = 0
        self.availability_zone = None

    def __repr__(self):
        return 'Subnet:%s' % self.id

    def endElement(self, name, value, connection):
        if name == 'subnetId':
            self.id = value
        else:
            if name == 'vpcId':
                self.vpc_id = value
            else:
                if name == 'state':
                    self.state = value
                else:
                    if name == 'cidrBlock':
                        self.cidr_block = value
                    else:
                        if name == 'availableIpAddressCount':
                            self.available_ip_address_count = int(value)
                        else:
                            if name == 'availabilityZone':
                                self.availability_zone = value
                            else:
                                setattr(self, name, value)