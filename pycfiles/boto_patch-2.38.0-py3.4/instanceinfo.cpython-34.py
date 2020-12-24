# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/instanceinfo.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1893 bytes


class InstanceInfo(object):
    __doc__ = '\n    Represents an EC2 Instance status response from CloudWatch\n    '

    def __init__(self, connection=None, id=None, state=None):
        """
        :ivar str id: The instance's EC2 ID.
        :ivar str state: Specifies the current status of the instance.
        """
        self.connection = connection
        self.id = id
        self.state = state

    def __repr__(self):
        return 'InstanceInfo:%s' % self.id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'instanceId' or name == 'InstanceId':
            self.id = value
        else:
            if name == 'state':
                self.state = value
            else:
                setattr(self, name, value)