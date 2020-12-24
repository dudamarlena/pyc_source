# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/spotpricehistory.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2093 bytes
__doc__ = '\nRepresents an EC2 Spot Instance Request\n'
from boto.ec2.ec2object import EC2Object

class SpotPriceHistory(EC2Object):

    def __init__(self, connection=None):
        super(SpotPriceHistory, self).__init__(connection)
        self.price = 0.0
        self.instance_type = None
        self.product_description = None
        self.timestamp = None
        self.availability_zone = None

    def __repr__(self):
        return 'SpotPriceHistory(%s):%2f' % (self.instance_type, self.price)

    def endElement(self, name, value, connection):
        if name == 'instanceType':
            self.instance_type = value
        else:
            if name == 'spotPrice':
                self.price = float(value)
            else:
                if name == 'productDescription':
                    self.product_description = value
                else:
                    if name == 'timestamp':
                        self.timestamp = value
                    else:
                        if name == 'availabilityZone':
                            self.availability_zone = value
                        else:
                            setattr(self, name, value)