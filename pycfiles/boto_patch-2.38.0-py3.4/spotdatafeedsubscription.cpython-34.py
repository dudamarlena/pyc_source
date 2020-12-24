# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/spotdatafeedsubscription.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2434 bytes
"""
Represents an EC2 Spot Instance Datafeed Subscription
"""
from boto.ec2.ec2object import EC2Object
from boto.ec2.spotinstancerequest import SpotInstanceStateFault

class SpotDatafeedSubscription(EC2Object):

    def __init__(self, connection=None, owner_id=None, bucket=None, prefix=None, state=None, fault=None):
        super(SpotDatafeedSubscription, self).__init__(connection)
        self.owner_id = owner_id
        self.bucket = bucket
        self.prefix = prefix
        self.state = state
        self.fault = fault

    def __repr__(self):
        return 'SpotDatafeedSubscription:%s' % self.bucket

    def startElement(self, name, attrs, connection):
        if name == 'fault':
            self.fault = SpotInstanceStateFault()
            return self.fault
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'ownerId':
            self.owner_id = value
        else:
            if name == 'bucket':
                self.bucket = value
            else:
                if name == 'prefix':
                    self.prefix = value
                else:
                    if name == 'state':
                        self.state = value
                    else:
                        setattr(self, name, value)

    def delete(self, dry_run=False):
        return self.connection.delete_spot_datafeed_subscription(dry_run=dry_run)