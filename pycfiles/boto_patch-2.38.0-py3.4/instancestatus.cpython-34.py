# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/instancestatus.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6854 bytes


class Details(dict):
    __doc__ = '\n    A dict object that contains name/value pairs which provide\n    more detailed information about the status of the system\n    or the instance.\n    '

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'name':
            self._name = value
        else:
            if name == 'status':
                self[self._name] = value
            else:
                setattr(self, name, value)


class Event(object):
    __doc__ = '\n    A status event for an instance.\n\n    :ivar code: A string indicating the event type.\n    :ivar description: A string describing the reason for the event.\n    :ivar not_before: A datestring describing the earliest time for\n        the event.\n    :ivar not_after: A datestring describing the latest time for\n        the event.\n    '

    def __init__(self, code=None, description=None, not_before=None, not_after=None):
        self.code = code
        self.description = description
        self.not_before = not_before
        self.not_after = not_after

    def __repr__(self):
        return 'Event:%s' % self.code

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'code':
            self.code = value
        else:
            if name == 'description':
                self.description = value
            else:
                if name == 'notBefore':
                    self.not_before = value
                else:
                    if name == 'notAfter':
                        self.not_after = value
                    else:
                        setattr(self, name, value)


class Status(object):
    __doc__ = '\n    A generic Status object used for system status and instance status.\n\n    :ivar status: A string indicating overall status.\n    :ivar details: A dict containing name-value pairs which provide\n        more details about the current status.\n    '

    def __init__(self, status=None, details=None):
        self.status = status
        if not details:
            details = Details()
        self.details = details

    def __repr__(self):
        return 'Status:%s' % self.status

    def startElement(self, name, attrs, connection):
        if name == 'details':
            return self.details

    def endElement(self, name, value, connection):
        if name == 'status':
            self.status = value
        else:
            setattr(self, name, value)


class EventSet(list):

    def startElement(self, name, attrs, connection):
        if name == 'item':
            event = Event()
            self.append(event)
            return event
        else:
            return

    def endElement(self, name, value, connection):
        setattr(self, name, value)


class InstanceStatus(object):
    __doc__ = '\n    Represents an EC2 Instance status as reported by\n    DescribeInstanceStatus request.\n\n    :ivar id: The instance identifier.\n    :ivar zone: The availability zone of the instance.\n    :ivar events: A list of events relevant to the instance.\n    :ivar state_code: An integer representing the current state\n        of the instance.\n    :ivar state_name: A string describing the current state\n        of the instance.\n    :ivar system_status: A Status object that reports impaired\n        functionality that stems from issues related to the systems\n        that support an instance, such as such as hardware failures\n        and network connectivity problems.\n    :ivar instance_status: A Status object that reports impaired\n        functionality that arises from problems internal to the instance.\n    '

    def __init__(self, id=None, zone=None, events=None, state_code=None, state_name=None):
        self.id = id
        self.zone = zone
        self.events = events
        self.state_code = state_code
        self.state_name = state_name
        self.system_status = Status()
        self.instance_status = Status()

    def __repr__(self):
        return 'InstanceStatus:%s' % self.id

    def startElement(self, name, attrs, connection):
        if name == 'eventsSet':
            self.events = EventSet()
            return self.events
        else:
            if name == 'systemStatus':
                return self.system_status
            if name == 'instanceStatus':
                return self.instance_status
            return

    def endElement(self, name, value, connection):
        if name == 'instanceId':
            self.id = value
        else:
            if name == 'availabilityZone':
                self.zone = value
            else:
                if name == 'code':
                    self.state_code = int(value)
                else:
                    if name == 'name':
                        self.state_name = value
                    else:
                        setattr(self, name, value)


class InstanceStatusSet(list):
    __doc__ = '\n    A list object that contains the results of a call to\n    DescribeInstanceStatus request.  Each element of the\n    list will be an InstanceStatus object.\n\n    :ivar next_token: If the response was truncated by\n        the EC2 service, the next_token attribute of the\n        object will contain the string that needs to be\n        passed in to the next request to retrieve the next\n        set of results.\n    '

    def __init__(self, connection=None):
        list.__init__(self)
        self.connection = connection
        self.next_token = None

    def startElement(self, name, attrs, connection):
        if name == 'item':
            status = InstanceStatus()
            self.append(status)
            return status
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'nextToken':
            self.next_token = value
        setattr(self, name, value)