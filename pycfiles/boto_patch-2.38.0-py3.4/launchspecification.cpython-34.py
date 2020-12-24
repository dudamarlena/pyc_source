# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/launchspecification.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3829 bytes
"""
Represents a launch specification for Spot instances.
"""
from boto.ec2.ec2object import EC2Object
from boto.resultset import ResultSet
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.group import Group
from boto.ec2.instance import SubParse

class GroupList(list):

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'groupId':
            self.append(value)


class LaunchSpecification(EC2Object):

    def __init__(self, connection=None):
        super(LaunchSpecification, self).__init__(connection)
        self.key_name = None
        self.instance_type = None
        self.image_id = None
        self.groups = []
        self.placement = None
        self.kernel = None
        self.ramdisk = None
        self.monitored = False
        self.subnet_id = None
        self._in_monitoring_element = False
        self.block_device_mapping = None
        self.instance_profile = None
        self.ebs_optimized = False

    def __repr__(self):
        return 'LaunchSpecification(%s)' % self.image_id

    def startElement(self, name, attrs, connection):
        if name == 'groupSet':
            self.groups = ResultSet([('item', Group)])
            return self.groups
        if name == 'monitoring':
            self._in_monitoring_element = True
        else:
            if name == 'blockDeviceMapping':
                self.block_device_mapping = BlockDeviceMapping()
                return self.block_device_mapping
            else:
                if name == 'iamInstanceProfile':
                    self.instance_profile = SubParse('iamInstanceProfile')
                    return self.instance_profile
                return

    def endElement(self, name, value, connection):
        if name == 'imageId':
            self.image_id = value
        else:
            if name == 'keyName':
                self.key_name = value
            else:
                if name == 'instanceType':
                    self.instance_type = value
                else:
                    if name == 'availabilityZone':
                        self.placement = value
                    else:
                        if name == 'placement':
                            pass
                        else:
                            if name == 'kernelId':
                                self.kernel = value
                            else:
                                if name == 'ramdiskId':
                                    self.ramdisk = value
                                else:
                                    if name == 'subnetId':
                                        self.subnet_id = value
                                    else:
                                        if name == 'state':
                                            if self._in_monitoring_element:
                                                if value == 'enabled':
                                                    self.monitored = True
                                                self._in_monitoring_element = False
                                        else:
                                            if name == 'ebsOptimized':
                                                self.ebs_optimized = value == 'true'
                                            else:
                                                setattr(self, name, value)