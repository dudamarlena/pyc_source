# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/vpc/vpc_peering_connection.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 5423 bytes
__doc__ = '\nRepresents a VPC Peering Connection.\n'
from boto.ec2.ec2object import TaggedEC2Object

class VpcInfo(object):

    def __init__(self):
        """
        Information on peer Vpc.
        
        :ivar id: The unique ID of peer Vpc.
        :ivar owner_id: Owner of peer Vpc.
        :ivar cidr_block: CIDR Block of peer Vpc.
        """
        self.vpc_id = None
        self.owner_id = None
        self.cidr_block = None

    def __repr__(self):
        return 'VpcInfo:%s' % self.vpc_id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'vpcId':
            self.vpc_id = value
        else:
            if name == 'ownerId':
                self.owner_id = value
            else:
                if name == 'cidrBlock':
                    self.cidr_block = value
                else:
                    setattr(self, name, value)


class VpcPeeringConnectionStatus(object):
    """VpcPeeringConnectionStatus"""

    def __init__(self, code=0, message=None):
        self.code = code
        self.message = message

    def __repr__(self):
        return '%s(%d)' % (self.code, self.message)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'code':
            self.code = value
        else:
            if name == 'message':
                self.message = value
            else:
                setattr(self, name, value)


class VpcPeeringConnection(TaggedEC2Object):

    def __init__(self, connection=None):
        """
        Represents a VPC peering connection.

        :ivar id: The unique ID of the VPC peering connection.
        :ivar accepter_vpc_info: Information on peer Vpc.
        :ivar requester_vpc_info: Information on requester Vpc.
        :ivar expiration_time: The expiration date and time for the VPC peering connection.
        :ivar status_code: The status of the VPC peering connection.
        :ivar status_message: A message that provides more information about the status of the VPC peering connection, if applicable.
        """
        super(VpcPeeringConnection, self).__init__(connection)
        self.id = None
        self.accepter_vpc_info = VpcInfo()
        self.requester_vpc_info = VpcInfo()
        self.expiration_time = None
        self._status = VpcPeeringConnectionStatus()

    @property
    def status_code(self):
        return self._status.code

    @property
    def status_message(self):
        return self._status.message

    def __repr__(self):
        return 'VpcPeeringConnection:%s' % self.id

    def startElement(self, name, attrs, connection):
        retval = super(VpcPeeringConnection, self).startElement(name, attrs, connection)
        if retval is not None:
            return retval
        if name == 'requesterVpcInfo':
            return self.requester_vpc_info
        if name == 'accepterVpcInfo':
            return self.accepter_vpc_info
        if name == 'status':
            return self._status

    def endElement(self, name, value, connection):
        if name == 'vpcPeeringConnectionId':
            self.id = value
        else:
            if name == 'expirationTime':
                self.expiration_time = value
            else:
                setattr(self, name, value)

    def delete(self):
        return self.connection.delete_vpc_peering_connection(self.id)

    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False, dry_run=False):
        vpc_peering_connection_list = self.connection.get_all_vpc_peering_connections([
         self.id], dry_run=dry_run)
        if len(vpc_peering_connection_list):
            updated_vpc_peering_connection = vpc_peering_connection_list[0]
            self._update(updated_vpc_peering_connection)
        elif validate:
            raise ValueError('%s is not a valid VpcPeeringConnection ID' % (self.id,))
        return self.status_code