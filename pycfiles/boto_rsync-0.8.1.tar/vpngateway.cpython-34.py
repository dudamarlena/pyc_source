# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/vpngateway.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2853 bytes
__doc__ = '\nRepresents a Vpn Gateway\n'
from boto.ec2.ec2object import TaggedEC2Object

class Attachment(object):

    def __init__(self, connection=None):
        self.vpc_id = None
        self.state = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'vpcId':
            self.vpc_id = value
        else:
            if name == 'state':
                self.state = value
            else:
                setattr(self, name, value)


class VpnGateway(TaggedEC2Object):

    def __init__(self, connection=None):
        super(VpnGateway, self).__init__(connection)
        self.id = None
        self.type = None
        self.state = None
        self.availability_zone = None
        self.attachments = []

    def __repr__(self):
        return 'VpnGateway:%s' % self.id

    def startElement(self, name, attrs, connection):
        retval = super(VpnGateway, self).startElement(name, attrs, connection)
        if retval is not None:
            return retval
        if name == 'item':
            att = Attachment()
            self.attachments.append(att)
            return att

    def endElement(self, name, value, connection):
        if name == 'vpnGatewayId':
            self.id = value
        else:
            if name == 'type':
                self.type = value
            else:
                if name == 'state':
                    self.state = value
                else:
                    if name == 'availabilityZone':
                        self.availability_zone = value
                    else:
                        if name == 'attachments':
                            pass
                        else:
                            setattr(self, name, value)

    def attach(self, vpc_id, dry_run=False):
        return self.connection.attach_vpn_gateway(self.id, vpc_id, dry_run=dry_run)