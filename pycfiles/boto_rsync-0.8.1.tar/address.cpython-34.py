# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/address.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 5348 bytes
from boto.ec2.ec2object import EC2Object

class Address(EC2Object):
    """Address"""

    def __init__(self, connection=None, public_ip=None, instance_id=None):
        super(Address, self).__init__(connection)
        self.connection = connection
        self.public_ip = public_ip
        self.instance_id = instance_id
        self.domain = None
        self.allocation_id = None
        self.association_id = None
        self.network_interface_id = None
        self.network_interface_owner_id = None
        self.private_ip_address = None

    def __repr__(self):
        return 'Address:%s' % self.public_ip

    def endElement(self, name, value, connection):
        if name == 'publicIp':
            self.public_ip = value
        else:
            if name == 'instanceId':
                self.instance_id = value
            else:
                if name == 'domain':
                    self.domain = value
                else:
                    if name == 'allocationId':
                        self.allocation_id = value
                    else:
                        if name == 'associationId':
                            self.association_id = value
                        else:
                            if name == 'networkInterfaceId':
                                self.network_interface_id = value
                            else:
                                if name == 'networkInterfaceOwnerId':
                                    self.network_interface_owner_id = value
                                else:
                                    if name == 'privateIpAddress':
                                        self.private_ip_address = value
                                    else:
                                        setattr(self, name, value)

    def release(self, dry_run=False):
        """
        Free up this Elastic IP address.
        :see: :meth:`boto.ec2.connection.EC2Connection.release_address`
        """
        if self.allocation_id:
            return self.connection.release_address(allocation_id=self.allocation_id, dry_run=dry_run)
        else:
            return self.connection.release_address(public_ip=self.public_ip, dry_run=dry_run)

    delete = release

    def associate(self, instance_id=None, network_interface_id=None, private_ip_address=None, allow_reassociation=False, dry_run=False):
        """
        Associate this Elastic IP address with a currently running instance.
        :see: :meth:`boto.ec2.connection.EC2Connection.associate_address`
        """
        if self.allocation_id:
            return self.connection.associate_address(instance_id=instance_id, public_ip=self.public_ip, allocation_id=self.allocation_id, network_interface_id=network_interface_id, private_ip_address=private_ip_address, allow_reassociation=allow_reassociation, dry_run=dry_run)
        return self.connection.associate_address(instance_id=instance_id, public_ip=self.public_ip, network_interface_id=network_interface_id, private_ip_address=private_ip_address, allow_reassociation=allow_reassociation, dry_run=dry_run)

    def disassociate(self, dry_run=False):
        """
        Disassociate this Elastic IP address from a currently running instance.
        :see: :meth:`boto.ec2.connection.EC2Connection.disassociate_address`
        """
        if self.association_id:
            return self.connection.disassociate_address(association_id=self.association_id, dry_run=dry_run)
        else:
            return self.connection.disassociate_address(public_ip=self.public_ip, dry_run=dry_run)