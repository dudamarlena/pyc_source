# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/spotinstancerequest.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7288 bytes
"""
Represents an EC2 Spot Instance Request
"""
from boto.ec2.ec2object import TaggedEC2Object
from boto.ec2.launchspecification import LaunchSpecification

class SpotInstanceStateFault(object):
    __doc__ = '\n    The fault codes for the Spot Instance request, if any.\n\n    :ivar code: The reason code for the Spot Instance state change.\n    :ivar message: The message for the Spot Instance state change.\n    '

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
    __doc__ = '\n    Contains the status of a Spot Instance Request.\n\n    :ivar code: Status code of the request.\n    :ivar message: The description for the status code for the Spot request.\n    :ivar update_time: Time the status was stated.\n    '

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
    __doc__ = '\n\n    :ivar id: The ID of the Spot Instance Request.\n    :ivar price: The maximum hourly price for any Spot Instance launched to\n        fulfill the request.\n    :ivar type: The Spot Instance request type.\n    :ivar state: The state of the Spot Instance request.\n    :ivar fault: The fault codes for the Spot Instance request, if any.\n    :ivar valid_from: The start date of the request. If this is a one-time\n        request, the request becomes active at this date and time and remains\n        active until all instances launch, the request expires, or the request is\n        canceled. If the request is persistent, the request becomes active at this\n        date and time and remains active until it expires or is canceled.\n    :ivar valid_until: The end date of the request. If this is a one-time\n        request, the request remains active until all instances launch, the request\n        is canceled, or this date is reached. If the request is persistent, it\n        remains active until it is canceled or this date is reached.\n    :ivar launch_group: The instance launch group. Launch groups are Spot\n        Instances that launch together and terminate together.\n    :ivar launched_availability_zone: foo\n    :ivar product_description: The Availability Zone in which the bid is\n        launched.\n    :ivar availability_zone_group: The Availability Zone group. If you specify\n        the same Availability Zone group for all Spot Instance requests, all Spot\n        Instances are launched in the same Availability Zone.\n    :ivar create_time: The time stamp when the Spot Instance request was\n        created.\n    :ivar launch_specification: Additional information for launching instances.\n    :ivar instance_id: The instance ID, if an instance has been launched to\n        fulfill the Spot Instance request.\n    :ivar status: The status code and status message describing the Spot\n        Instance request.\n\n    '

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