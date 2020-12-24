# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/autoscale/activity.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3058 bytes
from datetime import datetime

class Activity(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.start_time = None
        self.end_time = None
        self.activity_id = None
        self.progress = None
        self.status_code = None
        self.cause = None
        self.description = None
        self.status_message = None
        self.group_name = None

    def __repr__(self):
        return 'Activity<%s>: For group:%s, progress:%s, cause:%s' % (self.activity_id,
         self.group_name,
         self.status_message,
         self.cause)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'ActivityId':
            self.activity_id = value
        else:
            if name == 'AutoScalingGroupName':
                self.group_name = value
            elif name == 'StartTime':
                try:
                    self.start_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    self.start_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

            elif name == 'EndTime':
                try:
                    self.end_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    self.end_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

            else:
                if name == 'Progress':
                    self.progress = value
                else:
                    if name == 'Cause':
                        self.cause = value
                    else:
                        if name == 'Description':
                            self.description = value
                        else:
                            if name == 'StatusMessage':
                                self.status_message = value
                            else:
                                if name == 'StatusCode':
                                    self.status_code = value
                                else:
                                    setattr(self, name, value)