# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/placementgroup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2002 bytes
__doc__ = '\nRepresents an EC2 Placement Group\n'
from boto.ec2.ec2object import EC2Object
from boto.exception import BotoClientError

class PlacementGroup(EC2Object):

    def __init__(self, connection=None, name=None, strategy=None, state=None):
        super(PlacementGroup, self).__init__(connection)
        self.name = name
        self.strategy = strategy
        self.state = state

    def __repr__(self):
        return 'PlacementGroup:%s' % self.name

    def endElement(self, name, value, connection):
        if name == 'groupName':
            self.name = value
        else:
            if name == 'strategy':
                self.strategy = value
            else:
                if name == 'state':
                    self.state = value
                else:
                    setattr(self, name, value)

    def delete(self, dry_run=False):
        return self.connection.delete_placement_group(self.name, dry_run=dry_run)