# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/instancetype.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2273 bytes
from boto.ec2.ec2object import EC2Object

class InstanceType(EC2Object):
    """InstanceType"""

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