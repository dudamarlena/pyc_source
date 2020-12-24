# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/internetgateway.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2585 bytes
__doc__ = '\nRepresents an Internet Gateway\n'
from boto.ec2.ec2object import TaggedEC2Object
from boto.resultset import ResultSet

class InternetGateway(TaggedEC2Object):

    def __init__(self, connection=None):
        super(InternetGateway, self).__init__(connection)
        self.id = None
        self.attachments = []

    def __repr__(self):
        return 'InternetGateway:%s' % self.id

    def startElement(self, name, attrs, connection):
        result = super(InternetGateway, self).startElement(name, attrs, connection)
        if result is not None:
            return result
        else:
            if name == 'attachmentSet':
                self.attachments = ResultSet([('item', InternetGatewayAttachment)])
                return self.attachments
            return

    def endElement(self, name, value, connection):
        if name == 'internetGatewayId':
            self.id = value
        else:
            setattr(self, name, value)


class InternetGatewayAttachment(object):

    def __init__(self, connection=None):
        self.vpc_id = None
        self.state = None

    def __repr__(self):
        return 'InternetGatewayAttachment:%s' % self.vpc_id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'vpcId':
            self.vpc_id = value
        elif name == 'state':
            self.state = value