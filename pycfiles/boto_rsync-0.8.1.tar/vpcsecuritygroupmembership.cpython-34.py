# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/vpcsecuritygroupmembership.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3131 bytes
__doc__ = '\nRepresents a VPCSecurityGroupMembership\n'

class VPCSecurityGroupMembership(object):
    """VPCSecurityGroupMembership"""

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