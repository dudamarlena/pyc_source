# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/instanceinfo.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1893 bytes


class InstanceInfo(object):
    """InstanceInfo"""

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