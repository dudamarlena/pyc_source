# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/vpcsecuritygroupmembership.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3131 bytes
"""
Represents a VPCSecurityGroupMembership
"""

class VPCSecurityGroupMembership(object):
    __doc__ = '\n    Represents VPC Security Group that this RDS database is a member of\n\n    Properties reference available from the AWS documentation at\n    http://docs.aws.amazon.com/AmazonRDS/latest/APIReference/    API_VpcSecurityGroupMembership.html\n\n    Example::\n        pri = "sg-abcdefgh"\n        sec = "sg-hgfedcba"\n\n        # Create with list of str\n        db = c.create_dbinstance(... vpc_security_groups=[pri], ... )\n\n        # Modify with list of str\n        db.modify(... vpc_security_groups=[pri,sec], ... )\n\n        # Create with objects\n        memberships = []\n        membership = VPCSecurityGroupMembership()\n        membership.vpc_group = pri\n        memberships.append(membership)\n\n        db = c.create_dbinstance(... vpc_security_groups=memberships, ... )\n\n        # Modify with objects\n        memberships = d.vpc_security_groups\n        membership = VPCSecurityGroupMembership()\n        membership.vpc_group = sec\n        memberships.append(membership)\n\n        db.modify(...  vpc_security_groups=memberships, ... )\n\n    :ivar connection: :py:class:`boto.rds.RDSConnection` associated with the\n        current object\n    :ivar vpc_group: This id of the VPC security group\n    :ivar status: Status of the VPC security group membership\n        <boto.ec2.securitygroup.SecurityGroup>` objects that this RDS Instance\n        is a member of\n    '

    def __init__(self, connection=None, status=None, vpc_group=None):
        self.connection = connection
        self.status = status
        self.vpc_group = vpc_group

    def __repr__(self):
        return 'VPCSecurityGroupMembership:%s' % self.vpc_group

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'VpcSecurityGroupId':
            self.vpc_group = value
        else:
            if name == 'Status':
                self.status = value
            else:
                setattr(self, name, value)