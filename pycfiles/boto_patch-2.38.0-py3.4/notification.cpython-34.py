# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/mturk/notification.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4194 bytes
"""
Provides NotificationMessage and Event classes, with utility methods, for
implementations of the Mechanical Turk Notification API.
"""
import hmac
try:
    from hashlib import sha1 as sha
except ImportError:
    import sha

import base64, re

class NotificationMessage(object):
    NOTIFICATION_WSDL = 'http://mechanicalturk.amazonaws.com/AWSMechanicalTurk/2006-05-05/AWSMechanicalTurkRequesterNotification.wsdl'
    NOTIFICATION_VERSION = '2006-05-05'
    SERVICE_NAME = 'AWSMechanicalTurkRequesterNotification'
    OPERATION_NAME = 'Notify'
    EVENT_PATTERN = 'Event\\.(?P<n>\\d+)\\.(?P<param>\\w+)'
    EVENT_RE = re.compile(EVENT_PATTERN)

    def __init__(self, d):
        """
        Constructor; expects parameter d to be a dict of string parameters from a REST transport notification message
        """
        self.signature = d['Signature']
        self.timestamp = d['Timestamp']
        self.version = d['Version']
        assert d['method'] == NotificationMessage.OPERATION_NAME, "Method should be '%s'" % NotificationMessage.OPERATION_NAME
        self.events = []
        events_dict = {}
        if 'Event' in d:
            events_dict = d['Event']
        else:
            for k in d:
                v = d[k]
                if k.startswith('Event.'):
                    ed = NotificationMessage.EVENT_RE.search(k).groupdict()
                    n = int(ed['n'])
                    param = str(ed['param'])
                    if n not in events_dict:
                        events_dict[n] = {}
                    events_dict[n][param] = v
                    continue

        for n in events_dict:
            self.events.append(Event(events_dict[n]))

    def verify(self, secret_key):
        """
        Verifies the authenticity of a notification message.

        TODO: This is doing a form of authentication and
              this functionality should really be merged
              with the pluggable authentication mechanism
              at some point.
        """
        verification_input = NotificationMessage.SERVICE_NAME
        verification_input += NotificationMessage.OPERATION_NAME
        verification_input += self.timestamp
        h = hmac.new(key=secret_key, digestmod=sha)
        h.update(verification_input)
        signature_calc = base64.b64encode(h.digest())
        return self.signature == signature_calc


class Event(object):

    def __init__(self, d):
        self.event_type = d['EventType']
        self.event_time_str = d['EventTime']
        self.hit_type = d['HITTypeId']
        self.hit_id = d['HITId']
        if 'AssignmentId' in d:
            self.assignment_id = d['AssignmentId']

    def __repr__(self):
        return '<boto.mturk.notification.Event: %s for HIT # %s>' % (self.event_type, self.hit_id)