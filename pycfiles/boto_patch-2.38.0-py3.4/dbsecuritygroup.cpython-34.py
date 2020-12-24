# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/dbsecuritygroup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6651 bytes
"""
Represents an DBSecurityGroup
"""
from boto.ec2.securitygroup import SecurityGroup

class DBSecurityGroup(object):
    __doc__ = "\n    Represents an RDS database security group\n\n    Properties reference available from the AWS documentation at\n    http://docs.amazonwebservices.com/AmazonRDS/latest/APIReference/API_DeleteDBSecurityGroup.html\n\n    :ivar Status: The current status of the security group. Possible values are\n        [ active, ? ]. Reference documentation lacks specifics of possibilities\n    :ivar connection: :py:class:`boto.rds.RDSConnection` associated with the current object\n    :ivar description: The description of the security group\n    :ivar ec2_groups: List of :py:class:`EC2 Security Group\n        <boto.ec2.securitygroup.SecurityGroup>` objects that this security\n        group PERMITS\n    :ivar ip_ranges: List of :py:class:`boto.rds.dbsecuritygroup.IPRange`\n        objects (containing CIDR addresses) that this security group PERMITS\n    :ivar name: Name of the security group\n    :ivar owner_id: ID of the owner of the security group. Can be 'None'\n    "

    def __init__(self, connection=None, owner_id=None, name=None, description=None):
        self.connection = connection
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.ec2_groups = []
        self.ip_ranges = []

    def __repr__(self):
        return 'DBSecurityGroup:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'IPRange':
            cidr = IPRange(self)
            self.ip_ranges.append(cidr)
            return cidr
        else:
            if name == 'EC2SecurityGroup':
                ec2_grp = EC2SecurityGroup(self)
                self.ec2_groups.append(ec2_grp)
                return ec2_grp
            return

    def endElement(self, name, value, connection):
        if name == 'OwnerId':
            self.owner_id = value
        else:
            if name == 'DBSecurityGroupName':
                self.name = value
            else:
                if name == 'DBSecurityGroupDescription':
                    self.description = value
                else:
                    if name == 'IPRanges':
                        pass
                    else:
                        setattr(self, name, value)

    def delete(self):
        return self.connection.delete_dbsecurity_group(self.name)

    def authorize(self, cidr_ip=None, ec2_group=None):
        """
        Add a new rule to this DBSecurity group.
        You need to pass in either a CIDR block to authorize or
        and EC2 SecurityGroup.

        :type cidr_ip: string
        :param cidr_ip: A valid CIDR IP range to authorize

        :type ec2_group: :class:`boto.ec2.securitygroup.SecurityGroup`
        :param ec2_group: An EC2 security group to authorize

        :rtype: bool
        :return: True if successful.
        """
        if isinstance(ec2_group, SecurityGroup):
            group_name = ec2_group.name
            group_owner_id = ec2_group.owner_id
        else:
            group_name = None
            group_owner_id = None
        return self.connection.authorize_dbsecurity_group(self.name, cidr_ip, group_name, group_owner_id)

    def revoke(self, cidr_ip=None, ec2_group=None):
        """
        Revoke access to a CIDR range or EC2 SecurityGroup.
        You need to pass in either a CIDR block or
        an EC2 SecurityGroup from which to revoke access.

        :type cidr_ip: string
        :param cidr_ip: A valid CIDR IP range to revoke

        :type ec2_group: :class:`boto.ec2.securitygroup.SecurityGroup`
        :param ec2_group: An EC2 security group to revoke

        :rtype: bool
        :return: True if successful.
        """
        if isinstance(ec2_group, SecurityGroup):
            group_name = ec2_group.name
            group_owner_id = ec2_group.owner_id
            return self.connection.revoke_dbsecurity_group(self.name, ec2_security_group_name=group_name, ec2_security_group_owner_id=group_owner_id)
        return self.connection.revoke_dbsecurity_group(self.name, cidr_ip=cidr_ip)


class IPRange(object):
    __doc__ = '\n    Describes a CIDR address range for use in a DBSecurityGroup\n\n    :ivar cidr_ip: IP Address range\n    '

    def __init__(self, parent=None):
        self.parent = parent
        self.cidr_ip = None
        self.status = None

    def __repr__(self):
        return 'IPRange:%s' % self.cidr_ip

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'CIDRIP':
            self.cidr_ip = value
        else:
            if name == 'Status':
                self.status = value
            else:
                setattr(self, name, value)


class EC2SecurityGroup(object):
    __doc__ = '\n    Describes an EC2 security group for use in a DBSecurityGroup\n    '

    def __init__(self, parent=None):
        self.parent = parent
        self.name = None
        self.owner_id = None

    def __repr__(self):
        return 'EC2SecurityGroup:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'EC2SecurityGroupName':
            self.name = value
        else:
            if name == 'EC2SecurityGroupOwnerId':
                self.owner_id = value
            else:
                setattr(self, name, value)