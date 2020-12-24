# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/spotinstancerequest.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7288 bytes
__doc__ = '\nRepresents an EC2 Spot Instance Request\n'
from boto.ec2.ec2object import TaggedEC2Object
from boto.ec2.launchspecification import LaunchSpecification

class SpotInstanceStateFault(object):
    """SpotInstanceStateFault"""

    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def __repr__(self):
        return '(%s, %s)' % (self.code, self.message)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'code':
            self.code = value
        elif name == 'message':
            self.message = value
        setattr(self, name, value)


class SpotInstanceStatus(object):
    """SpotInstanceStatus"""

    def __init__(self, code=None, update_time=None, message=None):
        self.code = code
        self.update_time = update_time
        self.message = message

    def __repr__(self):
        return '<Status: %s>' % self.code

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'code':
            self.code = value
        else:
            if name == 'message':
                self.message = value
            elif name == 'updateTime':
                self.update_time = value


class SpotInstanceRequest(TaggedEC2Object):
    """SpotInstanceRequest"""

    def __init__(self, connection=None):
        super(SpotInstanceRequest, self).__init__(connection)
        self.id = None
        self.price = None
        self.type = None
        self.state = None
        self.fault = None
        self.valid_from = None
        self.valid_until = None
        self.launch_group = None
        self.launched_availability_zone = None
        self.product_description = None
        self.availability_zone_group = None
        self.create_time = None
        self.launch_specification = None
        self.instance_id = None
        self.status = None

    def __repr__(self):
        return 'SpotInstanceRequest:%s' % self.id

    def startElement(self, name, attrs, connection):
        retval = super(SpotInstanceRequest, self).startElement(name, attrs, connection)
        if retval is not None:
            return retval
        else:
            if name == 'launchSpecification':
                self.launch_specification = LaunchSpecification(connection)
                return self.launch_specification
            if name == 'fault':
                self.fault = SpotInstanceStateFault()
                return self.fault
            if name == 'status':
                self.status = SpotInstanceStatus()
                return self.status
            return

    def endElement(self, name, value, connection):
        if name == 'spotInstanceRequestId':
            self.id = value
        else:
            if name == 'spotPrice':
                self.price = float(value)
            else:
                if name == 'type':
                    self.type = value
                else:
                    if name == 'state':
                        self.state = value
                    else:
                        if name == 'validFrom':
                            self.valid_from = value
                        else:
                            if name == 'validUntil':
                                self.valid_until = value
                            else:
                                if name == 'launchGroup':
                                    self.launch_group = value
                                else:
                                    if name == 'availabilityZoneGroup':
                                        self.availability_zone_group = value
                                    else:
                                        if name == 'launchedAvailabilityZone':
                                            self.launched_availability_zone = value
                                        else:
                                            if name == 'instanceId':
                                                self.instance_id = value
                                            else:
                                                if name == 'createTime':
                                                    self.create_time = value
                                                else:
                                                    if name == 'productDescription':
                                                        self.product_description = value
                                                    else:
                                                        setattr(self, name, value)

    def cancel(self, dry_run=False):
        self.connection.cancel_spot_instance_requests([
         self.id], dry_run=dry_run)