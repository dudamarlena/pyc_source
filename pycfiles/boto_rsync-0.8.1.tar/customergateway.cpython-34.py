# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/customergateway.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1968 bytes
__doc__ = '\nRepresents a Customer Gateway\n'
from boto.ec2.ec2object import TaggedEC2Object

class CustomerGateway(TaggedEC2Object):

    def __init__(self, connection=None):
        super(CustomerGateway, self).__init__(connection)
        self.id = None
        self.type = None
        self.state = None
        self.ip_address = None
        self.bgp_asn = None

    def __repr__(self):
        return 'CustomerGateway:%s' % self.id

    def endElement(self, name, value, connection):
        if name == 'customerGatewayId':
            self.id = value
        else:
            if name == 'ipAddress':
                self.ip_address = value
            else:
                if name == 'type':
                    self.type = value
                else:
                    if name == 'state':
                        self.state = value
                    else:
                        if name == 'bgpAsn':
                            self.bgp_asn = int(value)
                        else:
                            setattr(self, name, value)