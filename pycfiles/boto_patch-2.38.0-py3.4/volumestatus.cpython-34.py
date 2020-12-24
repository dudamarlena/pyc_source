# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/volumestatus.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6329 bytes
from boto.ec2.instancestatus import Status, Details

class Event(object):
    __doc__ = '\n    A status event for an instance.\n\n    :ivar type: The type of the event.\n    :ivar id: The ID of the event.\n    :ivar description: A string describing the reason for the event.\n    :ivar not_before: A datestring describing the earliest time for\n        the event.\n    :ivar not_after: A datestring describing the latest time for\n        the event.\n    '

    def __init__(self, type=None, id=None, description=None, not_before=None, not_after=None):
        self.type = type
        self.id = id
        self.description = description
        self.not_before = not_before
        self.not_after = not_after

    def __repr__(self):
        return 'Event:%s' % self.type

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'eventType':
            self.type = value
        else:
            if name == 'eventId':
                self.id = value
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


class Action(object):
    __doc__ = '\n    An action for an instance.\n\n    :ivar code: The code for the type of the action.\n    :ivar id: The ID of the event.\n    :ivar type: The type of the event.\n    :ivar description: A description of the action.\n    '

    def __init__(self, code=None, id=None, description=None, type=None):
        self.code = code
        self.id = id
        self.type = type
        self.description = description

    def __repr__(self):
        return 'Action:%s' % self.code

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'eventType':
            self.type = value
        else:
            if name == 'eventId':
                self.id = value
            else:
                if name == 'description':
                    self.description = value
                else:
                    if name == 'code':
                        self.code = value
                    else:
                        setattr(self, name, value)


class ActionSet(list):

    def startElement(self, name, attrs, connection):
        if name == 'item':
            action = Action()
            self.append(action)
            return action
        else:
            return

    def endElement(self, name, value, connection):
        setattr(self, name, value)


class VolumeStatus(object):
    __doc__ = '\n    Represents an EC2 Volume status as reported by\n    DescribeVolumeStatus request.\n\n    :ivar id: The volume identifier.\n    :ivar zone: The availability zone of the volume\n    :ivar volume_status: A Status object that reports impaired\n        functionality that arises from problems internal to the instance.\n    :ivar events: A list of events relevant to the instance.\n    :ivar actions: A list of events relevant to the instance.\n    '

    def __init__(self, id=None, zone=None):
        self.id = id
        self.zone = zone
        self.volume_status = Status()
        self.events = None
        self.actions = None

    def __repr__(self):
        return 'VolumeStatus:%s' % self.id

    def startElement(self, name, attrs, connection):
        if name == 'eventsSet':
            self.events = EventSet()
            return self.events
        else:
            if name == 'actionsSet':
                self.actions = ActionSet()
                return self.actions
            if name == 'volumeStatus':
                return self.volume_status
            return

    def endElement(self, name, value, connection):
        if name == 'volumeId':
            self.id = value
        else:
            if name == 'availabilityZone':
                self.zone = value
            else:
                setattr(self, name, value)


class VolumeStatusSet(list):
    __doc__ = '\n    A list object that contains the results of a call to\n    DescribeVolumeStatus request.  Each element of the\n    list will be an VolumeStatus object.\n\n    :ivar next_token: If the response was truncated by\n        the EC2 service, the next_token attribute of the\n        object will contain the string that needs to be\n        passed in to the next request to retrieve the next\n        set of results.\n    '

    def __init__(self, connection=None):
        list.__init__(self)
        self.connection = connection
        self.next_token = None

    def startElement(self, name, attrs, connection):
        if name == 'item':
            status = VolumeStatus()
            self.append(status)
            return status
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'NextToken':
            self.next_token = value
        setattr(self, name, value)