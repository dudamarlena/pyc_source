# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/instancestatus.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6854 bytes


class Details(dict):
    """Details"""

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
    """Event"""

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
    """Status"""

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
    """InstanceStatus"""

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
    """InstanceStatusSet"""

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