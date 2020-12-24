# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/instancetype.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2273 bytes
from boto.ec2.ec2object import EC2Object

class InstanceType(EC2Object):
    __doc__ = '\n    Represents an EC2 VM Type\n\n    :ivar name: The name of the vm type\n    :ivar cores: The number of cpu cores for this vm type\n    :ivar memory: The amount of memory in megabytes for this vm type\n    :ivar disk: The amount of disk space in gigabytes for this vm type\n    '

    def __init__(self, connection=None, name=None, cores=None, memory=None, disk=None):
        super(InstanceType, self).__init__(connection)
        self.connection = connection
        self.name = name
        self.cores = cores
        self.memory = memory
        self.disk = disk

    def __repr__(self):
        return 'InstanceType:%s-%s,%s,%s' % (self.name, self.cores,
         self.memory, self.disk)

    def endElement(self, name, value, connection):
        if name == 'name':
            self.name = value
        else:
            if name == 'cpu':
                self.cores = value
            else:
                if name == 'disk':
                    self.disk = value
                else:
                    if name == 'memory':
                        self.memory = value
                    else:
                        setattr(self, name, value)