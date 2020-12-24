# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/dbsubnetgroup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2825 bytes
"""
Represents an DBSubnetGroup
"""

class DBSubnetGroup(object):
    __doc__ = '\n    Represents an RDS database subnet group\n\n    Properties reference available from the AWS documentation at http://docs.amazonwebservices.com/AmazonRDS/latest/APIReference/API_DeleteDBSubnetGroup.html\n\n    :ivar status: The current status of the subnet group. Possibile values are [ active, ? ]. Reference documentation lacks specifics of possibilities\n    :ivar connection: boto.rds.RDSConnection associated with the current object\n    :ivar description: The description of the subnet group\n    :ivar subnet_ids: List of subnet identifiers in the group\n    :ivar name: Name of the subnet group\n    :ivar vpc_id: The ID of the VPC the subnets are inside\n    '

    def __init__(self, connection=None, name=None, description=None, subnet_ids=None):
        self.connection = connection
        self.name = name
        self.description = description
        if subnet_ids is not None:
            self.subnet_ids = subnet_ids
        else:
            self.subnet_ids = []
        self.vpc_id = None
        self.status = None

    def __repr__(self):
        return 'DBSubnetGroup:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'SubnetIdentifier':
            self.subnet_ids.append(value)
        else:
            if name == 'DBSubnetGroupName':
                self.name = value
            else:
                if name == 'DBSubnetGroupDescription':
                    self.description = value
                else:
                    if name == 'VpcId':
                        self.vpc_id = value
                    else:
                        if name == 'SubnetGroupStatus':
                            self.status = value
                        else:
                            setattr(self, name, value)